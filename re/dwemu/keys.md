# The two embedded keys

> The game proves it is talking to Demonware with two RSA public keys stored in its own image. Replace them in memory, and a server with the matching private keys is "Demonware". **Status:** Done, in game.

## In short

- Two RSA-2048 public keys sit in the image's read-only data, each as a 294-byte DER blob.
- One verifies the signature on the auth reply. The other belongs to the LSG handshake.
- cw-mod generates its own key pairs, and at start overwrites both blobs with its own public keys. Same length, same place: an in-place replace.
- The player's key files are the opt-in. No files, no patch, and the game is untouched.

## The keys

| Name | RVA | IDA address | Size | Used by |
|---|---|---|---|---|
| `g_dwAuthSigPubKey_DER` | 0xD9781B0 | 0x7FF72A5381B0 | 294 bytes | `DwAuth_VerifyReplySignature`: the `X-Signature` header of the auth reply |
| `g_lsgHandshakePubKey_DER` | 0xD977330 | 0x7FF72A537330 | 294 bytes | `Lsg_BuildHandshake_ParseBDDATA`: the LSG handshake |

A DER `SubjectPublicKeyInfo` for an RSA-2048 key with exponent 65537 always has this length and always starts with the same 24 bytes:

```text
30 82 01 22 30 0D 06 09 2A 86 48 86 F7 0D 01 01 01 05 00 03 82 01 0F 00
```

That prefix is how the patch knows it is pointed at a key and not at something else. In the retail image the two blobs hold the same key.

## The signature the auth key verifies

Read from `DwAuth_VerifyReplySignature` and the routine it calls:

| Parameter | Value |
|---|---|
| Scheme | RSASSA-PSS |
| Hash | SHA-256 |
| Mask function | MGF1 with SHA-256 |
| Salt length | **0** |
| Signed bytes | The raw response body, exactly as sent |
| Where | The `X-Signature` response header, base64 of 256 bytes |

A salt length of 0 makes the signature deterministic. The server signs the exact bytes it writes: sign first and then re-encode the JSON, and the signature is for another message.

## The LSG key

In the handshake as it runs on this build, the second key is not used as a key. The key schedule has a branch that stretches the session key with the DER blob as a **label**; the measured handshake takes the other branch and uses the session key as it is. See [The LSG connection](/re/dwemu/lsg.md). The blob is still replaced, so both branches would work.

## Functions

| Name | RVA | IDA address | Role |
|---|---|---|---|
| `DwAuth_VerifyReplySignature` | 0xD230F90 | 0x7FF729DF0F90 | Decodes the header, verifies the body |
| `Crypto_RsaPss_Verify` | 0xCE64210 | 0x7FF729A24210 | The PSS verify |
| `Crypto_RsaImportPubKey` | 0xD17AE60 | 0x7FF729D3AE60 | Imports a DER key. The fallback hook point if the patch were ever reverted. |
| `Lsg_BuildHandshake_ParseBDDATA` | 0xD227050 | 0x7FF729DE7050 | The LSG key schedule |

## What cw-mod does

`DwBackend::PatchEmbeddedKeys` in `client/game/dw_backend.cpp`, called once from the `Pointers` constructor:

1. Stop if `"backend"` is false.
2. Read `<game>\cw-mod\dwserver\auth_pub.der` and `lsg_pub.der`. Each must be exactly 294 bytes.
3. For each: compute the live address from the anchor and check it is inside the image.
4. Check the 24-byte prefix **at the target**. No prefix means another build: refuse.
5. Make the page writable, copy, restore the protection.
6. Read the bytes back and compare.

The backend counts as on only when the **auth** key was replaced. That one flag then decides the rest of the start: whether Demonware names are redirected, and whether `nodw` is cleared so the login runs. See [The boot profile](/re/client/boot-profile.md).

The log says `key replaced and verified` for each, or `read-back MISMATCH` if the protection ever restores the bytes.

## Making the keys

`tools/dwserver/gen_keys.py` writes everything into a `material` folder that is never committed:

| Output | Use |
|---|---|
| Two private keys | The server signs with them. They stay on the PC. |
| `auth_pub.der`, `lsg_pub.der` | Copied to `<game>\cw-mod\dwserver\` |
| A certificate authority, a leaf certificate, a revocation list | [TLS](/re/dwemu/redirect-tls.md) |

`tools/dwserver/selftest.py` signs a reply and verifies it with the same parameters the game uses. It needs no game.

## How we found it

- The auth reply handler rejects an unsigned reply before it reads a single field. Following the verify call down gave the PSS parameters and the address of the key.
- The second key was found the same way from the LSG handshake.
- A patch of read-only data under a protection that checksums code looked risky. The read-back check was written to find out, and it has passed.

## Limits

- The two addresses are for this build. The prefix check turns a mismatch into a safe refusal.
- Every PC that should talk to one backend needs that backend's public keys. In practice each PC runs its own backend with its own keys.

## See also

- [Auth](/re/dwemu/auth.md): the reply that is signed
- [The LSG connection](/re/dwemu/lsg.md)
- [dwserver](/guide/tools/dwserver.md): generating and installing the keys

<!-- sources: cw-mod client/game/dw_backend.cpp, dw_backend.hpp, client/game/dump_anchors.hpp (the key anchors), tools/dwserver/gen_keys.py, dwsign.py, lsgcrypto.py (the wrap branch), lsgserver.py (WRAP_CONFIRMED), tools/dwserver/README.md (risk notes) @ 36b1f18 + working tree, 2026-10-08 -->
