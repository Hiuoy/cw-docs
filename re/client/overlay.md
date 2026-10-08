# The overlay

> The in-game menu is ImGui drawn into the game's own D3D12 frame. This page covers how it gets its device, how it survives a resolution change, and why keystrokes leaked to the game until two more hooks went in. **Status:** Done.

## In short

- Three D3D12 functions are hooked through addresses read from a throwaway device's vtables.
- The overlay draws on the render thread and **never calls game code**: a button queues a closure, and the [game-thread tick](/re/client/overview.md) runs it.
- Before the game resizes its swapchain, the overlay lets go of every buffer it holds, or the resize fails and the game does not survive.
- Blocking window messages kept the mouse out of the game, but not the keyboard: the game reads keys two other ways.

## Getting the device

The game's device and swapchain are not exported, but their methods live in the same `d3d12.dll` and `dxgi.dll` for every object in the process. So the client creates a dummy window, device, command queue and swapchain, reads three vtable slots, and destroys them again.

| Method | Slot | Hooked to |
|---|---|---|
| `IDXGISwapChain::Present` | 8 | Capture the device, build the renderer, draw |
| `IDXGISwapChain::ResizeBuffers` | 13 | Tear the renderer down first |
| `ID3D12CommandQueue::ExecuteCommandLists` | 10 | Remember the first DIRECT queue the game uses |

ImGui's D3D12 backend must submit its command list on the game's own queue, which is why the third hook exists. The device comes from `swapChain->GetDevice` inside the first `Present` after a queue was seen.

## One frame

1. `Present` is called by the game.
2. If the swapchain is not the one the render targets were built from, or its size, format or buffer count changed, tear down and rebuild.
3. Start an ImGui frame. Draw the script messages, and the menu if it is open.
4. Transition the back buffer from present to render target, draw, transition back.
5. Execute the list on the game's queue, then call the real `Present`.

The script messages are the mirror of `iprintln` and `iprintlnbold`: the game draws a script's plain-text print as an empty box, so the client shows the text itself. See [The GSC VM](/re/engine/gsc-vm.md).

## Surviving a resize

DXGI refuses `ResizeBuffers` while anyone holds a reference to a back buffer, and the game does not handle that failure.

| Step | Detail |
|---|---|
| Wait for the GPU | Signal a fence and wait at most 1 second. Never hang the render thread. |
| Shut down ImGui's D3D12 backend | Only if it came up |
| Release | Back buffers, command allocators, the command list, both descriptor heaps, the fence |
| Keep | The ImGui context, the Win32 backend and the window hook, so the menu's state survives |

The next `Present` builds everything again. `Present` and `ResizeBuffers` run on different threads, so both take one lock.

## Input

The game's window procedure is replaced with `SetWindowLongPtrW`. Insert, on key-up, toggles the menu. While it is open, mouse and keyboard messages go to ImGui and are not passed on.

That was enough for the mouse. Typing in a text box still opened the scoreboard and fired the weapon.

| Path the game reads keys by | Why the window hook missed it | Fix |
|---|---|---|
| Window messages | | Consumed while the menu is open |
| `GetRawInputBuffer` | The game drains the raw-input queue in bulk. That never goes through the window procedure. | Call the original, so the queue is drained, then report **0 events**. Not calling it would leave a backlog that arrives when the menu closes. A size query (no buffer) passes through unchanged. |
| `GetAsyncKeyState` | The game also **polls** key state. There is no queue to starve and no message to swallow. | Answer 0, but only to callers **inside the game image**. ImGui polls too, for shift and the other modifiers. |

The caller test uses the hook's own return address: MinHook enters the detour with a jump, not a call, so the return address is the original caller's.

Both functions were found in the game's import table. See [Tools](/re/method/tooling.md).

## The action queue

```cpp
void Enqueue(std::function<void()> action);   // any thread
void DrainActions();                           // the game-thread tick
```

Every button that touches the game goes through it. Plain globals may be read from the render thread; calls may not be made.

## The tabs

One file per tab under `client/overlay/tabs/`. What each does is in the [overlay guide](/guide/overlay.md).

## Limits

- D3D12 only, which is all this game uses.
- If the renderer fails to build once, the overlay stays off for that session.
- The software cursor is drawn only while the menu is open.

## See also

- [The overlay, for players](/guide/overlay.md)
- [Hooking](/re/client/hooking.md)

<!-- sources: cw-mod client/overlay/d3d12_hook.cpp, menu.hpp, client/hooks/impl/patched/user32/GetRawInputBuffer.cpp, GetAsyncKeyState.cpp, client/hooks/hook.hpp @ 36b1f18 + working tree, 2026-10-08 -->
