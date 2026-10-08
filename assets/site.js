// Site configuration for docsify, and two small plugins of our own.
// Loaded before docsify itself (see index.html).
(function () {
  'use strict';

  var MERMAID_URL = 'https://cdn.jsdelivr.net/npm/mermaid@12.1.0/dist/mermaid.esm.min.mjs';

  // Diagrams: a ```mermaid block becomes a drawing. mermaid is large, so it is fetched only when a page
  // has such a block.
  function mermaidPlugin(hook) {
    var loading = null;

    function load() {
      if (!loading) {
        loading = import(MERMAID_URL).then(function (module) {
          var mermaid = module.default;
          var dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
          mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: dark ? 'dark' : 'neutral' });
          return mermaid;
        });
      }
      return loading;
    }

    hook.doneEach(function () {
      var blocks = document.querySelectorAll(
        '.markdown-section pre[data-lang="mermaid"], .markdown-section pre.language-mermaid'
      );
      if (!blocks.length) {
        return;
      }
      var nodes = [];
      blocks.forEach(function (pre) {
        var code = pre.querySelector('code');
        var div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = (code || pre).textContent;
        pre.replaceWith(div);
        nodes.push(div);
      });
      load()
        .then(function (mermaid) {
          return mermaid.run({ nodes: nodes });
        })
        .catch(function (error) {
          console.error('mermaid:', error);
        });
    });
  }

  // Sidebar: a group (a list item with a title and a nested list) folds. The group that holds the open
  // page is unfolded; a click on a group's title folds or unfolds it.
  function sidebarGroupsPlugin(hook) {
    function groups() {
      var found = [];
      document.querySelectorAll('.sidebar-nav > ul > li').forEach(function (item) {
        var list = item.querySelector(':scope > ul');
        var ownLink = item.querySelector(':scope > a');
        if (list && !ownLink) {
          found.push(item);
        }
      });
      return found;
    }

    function titleOf(item) {
      return item.querySelector(':scope > p, :scope > strong') || item.firstChild;
    }

    hook.doneEach(function () {
      var all = groups();
      if (all.length < 2) {
        return;
      }
      all.forEach(function (item) {
        item.classList.add('cw-group');
        var active = item.querySelector('li.active, a.active');
        if (!item.dataset.cwBound) {
          item.dataset.cwBound = '1';
          var title = titleOf(item);
          if (title && title.nodeType === 1) {
            title.classList.add('cw-group-title');
            title.setAttribute('role', 'button');
            title.setAttribute('tabindex', '0');
            var toggle = function () {
              item.classList.toggle('cw-folded');
            };
            title.addEventListener('click', toggle);
            title.addEventListener('keydown', function (event) {
              if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                toggle();
              }
            });
          }
          item.classList.toggle('cw-folded', !active);
        } else if (active) {
          item.classList.remove('cw-folded');
        }
      });
    });
  }

  window.$docsify = {
    name: 'cw-mod docs',
    repo: 'Hiuoy/cw-mod',
    loadSidebar: true,
    loadNavbar: true,
    mergeNavbar: true,
    subMaxLevel: 2,
    maxLevel: 3,
    auto2top: true,
    notFoundPage: true,
    relativePath: false,
    search: {
      paths: window.CW_DOCS_PAGES || 'auto',
      placeholder: 'Search the docs',
      noData: 'Nothing found',
      depth: 3,
      namespace: 'cw-docs',
      hideOtherSidebarContent: false
    },
    pagination: {
      previousText: 'Previous',
      nextText: 'Next',
      crossChapter: true,
      crossChapterText: true
    },
    copyCode: {
      buttonText: 'Copy',
      errorText: 'Error',
      successText: 'Copied'
    },
    tabs: {
      persist: true,
      sync: true,
      theme: 'classic',
      tabComments: true,
      tabHeadings: true
    },
    plugins: [mermaidPlugin, sidebarGroupsPlugin]
  };
})();
