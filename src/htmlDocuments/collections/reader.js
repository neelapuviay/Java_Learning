/**
 * Java Collections Documentation — Reader Engine
 * Provides multi-theme switching, typography controls, code copying,
 * reading progress bar, and completion tracking.
 */
(function () {
  'use strict';

  const STORAGE_KEYS = {
    theme: 'jvm_reader_theme',
    font: 'jvm_reader_font',
    size: 'jvm_reader_size',
    width: 'jvm_reader_width',
    completed: 'jvm_reader_completed'
  };

  // Default settings
  const DEFAULTS = {
    theme: 'sepia', // Warm paper mode is default for soothing eye comfort
    font: 'sans',   // Modern clean sans-serif for sharp technical legibility
    size: 'md',     // 17px standard comfortable reading size
    width: 'focus'  // 72ch ergonomic reading column width
  };

  function getStored(key, fallback) {
    try {
      return localStorage.getItem(key) || fallback;
    } catch (e) {
      return fallback;
    }
  }

  function setStored(key, val) {
    try {
      localStorage.setItem(key, val);
    } catch (e) {}
  }

  // Get current settings
  const currentSettings = {
    theme: getStored(STORAGE_KEYS.theme, DEFAULTS.theme),
    font: getStored(STORAGE_KEYS.font, DEFAULTS.font),
    size: getStored(STORAGE_KEYS.size, DEFAULTS.size),
    width: getStored(STORAGE_KEYS.width, DEFAULTS.width)
  };

  // Apply settings to document element
  function applySettings() {
    const doc = document.documentElement;
    doc.setAttribute('data-theme', currentSettings.theme);
    doc.setAttribute('data-font', currentSettings.font);
    doc.setAttribute('data-size', currentSettings.size);
    doc.setAttribute('data-width', currentSettings.width);

    // Sync active states on toolbar buttons if present
    document.querySelectorAll('[data-theme-set]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-theme-set') === currentSettings.theme);
    });
    document.querySelectorAll('[data-font-set]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-font-set') === currentSettings.font);
    });
    document.querySelectorAll('[data-size-set]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-size-set') === currentSettings.size);
    });
    document.querySelectorAll('[data-width-set]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-width-set') === currentSettings.width);
    });

    // Notify iframe or parent window
    broadcastSettings();
  }

  function broadcastSettings() {
    const msg = {
      type: 'JVM_READER_SETTINGS_CHANGE',
      settings: currentSettings
    };
    // If inside an iframe, tell parent
    if (window.parent && window.parent !== window) {
      window.parent.postMessage(msg, '*');
    }
    // If in parent window, tell iframe
    const frame = document.getElementById('content-frame');
    if (frame && frame.contentWindow) {
      try {
        frame.contentWindow.postMessage(msg, '*');
      } catch (e) {}
    }
  }

  // Listen for settings from parent or iframe
  window.addEventListener('message', function (event) {
    if (event.data && event.data.type === 'JVM_READER_SETTINGS_CHANGE') {
      const s = event.data.settings;
      if (s) {
        if (s.theme) currentSettings.theme = s.theme;
        if (s.font) currentSettings.font = s.font;
        if (s.size) currentSettings.size = s.size;
        if (s.width) currentSettings.width = s.width;

        const doc = document.documentElement;
        doc.setAttribute('data-theme', currentSettings.theme);
        doc.setAttribute('data-font', currentSettings.font);
        doc.setAttribute('data-size', currentSettings.size);
        doc.setAttribute('data-width', currentSettings.width);

        document.querySelectorAll('[data-theme-set]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-theme-set') === currentSettings.theme);
        });
        document.querySelectorAll('[data-font-set]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-font-set') === currentSettings.font);
        });
        document.querySelectorAll('[data-size-set]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-size-set') === currentSettings.size);
        });
        document.querySelectorAll('[data-width-set]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-width-set') === currentSettings.width);
        });
      }
    } else if (event.data && event.data.type === 'JVM_MODULE_COMPLETED') {
      updateSidebarProgress();
    }
  });

  // Export functions to window
  window.JvmReader = {
    setTheme: function (theme) {
      currentSettings.theme = theme;
      setStored(STORAGE_KEYS.theme, theme);
      applySettings();
    },
    setFont: function (font) {
      currentSettings.font = font;
      setStored(STORAGE_KEYS.font, font);
      applySettings();
    },
    setSize: function (size) {
      currentSettings.size = size;
      setStored(STORAGE_KEYS.size, size);
      applySettings();
    },
    cycleSize: function (direction) {
      const sizes = ['sm', 'md', 'lg', 'xl'];
      let idx = sizes.indexOf(currentSettings.size);
      if (idx === -1) idx = 1;
      if (direction === 'up' && idx < sizes.length - 1) idx++;
      if (direction === 'down' && idx > 0) idx--;
      this.setSize(sizes[idx]);
    },
    toggleWidth: function () {
      const newWidth = currentSettings.width === 'focus' ? 'wide' : 'focus';
      currentSettings.width = newWidth;
      setStored(STORAGE_KEYS.width, newWidth);
      applySettings();
    },
    getCompletedModules: function () {
      try {
        const raw = localStorage.getItem(STORAGE_KEYS.completed);
        return raw ? JSON.parse(raw) : [];
      } catch (e) {
        return [];
      }
    },
    markCompleted: function (moduleId) {
      const list = this.getCompletedModules();
      if (!list.includes(moduleId)) {
        list.push(moduleId);
        setStored(STORAGE_KEYS.completed, JSON.stringify(list));
      }
      if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'JVM_MODULE_COMPLETED', moduleId: moduleId }, '*');
      }
      updateSidebarProgress();
      updateCompleteButtonState(moduleId);
    },
    toggleCompleted: function (moduleId) {
      let list = this.getCompletedModules();
      if (list.includes(moduleId)) {
        list = list.filter(id => id !== moduleId);
      } else {
        list.push(moduleId);
      }
      setStored(STORAGE_KEYS.completed, JSON.stringify(list));
      if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'JVM_MODULE_COMPLETED', moduleId: moduleId }, '*');
      }
      updateSidebarProgress();
      updateCompleteButtonState(moduleId);
    }
  };

  // Update button state on current page if present
  function updateCompleteButtonState(moduleId) {
    const btn = document.querySelector('.btn-mark-complete');
    if (!btn) return;
    const list = window.JvmReader.getCompletedModules();
    const isDone = list.includes(moduleId);
    if (isDone) {
      btn.classList.add('completed');
      btn.innerHTML = '<span>✓</span> Completed!';
    } else {
      btn.classList.remove('completed');
      btn.innerHTML = '<span>○</span> Mark as Completed';
    }
  }

  // Update sidebar progress badges in index.html
  function updateSidebarProgress() {
    const completed = window.JvmReader.getCompletedModules();
    const moduleLinks = document.querySelectorAll('.portal-link[data-module-id]');
    
    moduleLinks.forEach(link => {
      const modId = link.getAttribute('data-module-id');
      let badge = link.querySelector('.complete-check');
      if (completed.includes(modId)) {
        if (!badge) {
          badge = document.createElement('span');
          badge.className = 'complete-check';
          badge.textContent = '✓';
          badge.title = 'Completed';
          link.appendChild(badge);
        }
        link.classList.add('is-completed');
      } else {
        if (badge) badge.remove();
        link.classList.remove('is-completed');
      }
    });

    // Update counter if present
    const countEl = document.getElementById('progress-counter');
    if (countEl) {
      const total = 7;
      const count = completed.length;
      countEl.textContent = `${count} of ${total} Completed`;
      const fillEl = document.getElementById('progress-fill-bar');
      if (fillEl) {
        fillEl.style.width = `${Math.round((count / total) * 100)}%`;
      }
    }
  }

  // Enhance code blocks with copy button and language tag
  function setupCodeBlocks() {
    document.querySelectorAll('pre').forEach(pre => {
      // Don't add if already wrapped
      if (pre.parentElement.classList.contains('code-block-wrapper')) return;

      const wrapper = document.createElement('div');
      wrapper.className = 'code-block-wrapper';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);

      // Header bar
      const header = document.createElement('div');
      header.className = 'code-block-header';

      // Detect language
      let lang = pre.getAttribute('data-lang') || 'Java';
      const codeText = pre.textContent || '';
      if (codeText.includes('class ') || codeText.includes('public static') || codeText.includes('List<') || codeText.includes('Map<')) {
        lang = 'Java';
      } else if (codeText.includes('Heap:') || codeText.includes('Stack:') || codeText.includes('0x') || codeText.includes('Memory:')) {
        lang = 'Memory Layout';
      }

      const langSpan = document.createElement('span');
      langSpan.className = 'code-lang-label';
      langSpan.textContent = lang;
      header.appendChild(langSpan);

      // Copy Button
      const copyBtn = document.createElement('button');
      copyBtn.className = 'code-copy-btn';
      copyBtn.setAttribute('type', 'button');
      copyBtn.innerHTML = '<span class="copy-icon">📋</span> Copy';
      copyBtn.addEventListener('click', function () {
        const textToCopy = pre.innerText.replace(/^\s*\d+:\s/gm, ''); // strip line numbers if any
        navigator.clipboard.writeText(textToCopy).then(() => {
          copyBtn.innerHTML = '<span class="copy-icon" style="color:var(--green)">✓</span> Copied!';
          copyBtn.classList.add('copied');
          setTimeout(() => {
            copyBtn.innerHTML = '<span class="copy-icon">📋</span> Copy';
            copyBtn.classList.remove('copied');
          }, 2000);
        }).catch(() => {
          copyBtn.textContent = 'Error';
        });
      });
      header.appendChild(copyBtn);

      wrapper.insertBefore(header, pre);
    });
  }

  // Setup reading scroll progress bar
  function setupReadingProgress() {
    // Only in content pages (not portal index frame)
    if (document.querySelector('.portal-container')) return;

    let bar = document.querySelector('.reading-progress-indicator');
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'reading-progress-indicator';
      document.body.prepend(bar);
    }

    function updateProgress() {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight <= 0) {
        bar.style.width = '0%';
        return;
      }
      const scrollPos = window.scrollY || window.pageYOffset || 0;
      const progress = Math.min(100, Math.max(0, (scrollPos / docHeight) * 100));
      bar.style.width = progress + '%';
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  // Setup expandable Knowledge Checks
  function setupKnowledgeChecks() {
    document.querySelectorAll('.quiz-box').forEach(box => {
      const toggle = box.querySelector('.quiz-toggle');
      const answer = box.querySelector('.quiz-answer');
      if (toggle && answer) {
        toggle.addEventListener('click', () => {
          const isOpen = box.classList.toggle('is-open');
          toggle.setAttribute('aria-expanded', isOpen);
          const icon = toggle.querySelector('.quiz-toggle-icon');
          if (icon) icon.textContent = isOpen ? '▲' : '▼';
        });
      }
    });
  }

  // Bind toolbar clicks
  function setupToolbarControls() {
    document.querySelectorAll('[data-theme-set]').forEach(btn => {
      btn.addEventListener('click', () => {
        window.JvmReader.setTheme(btn.getAttribute('data-theme-set'));
      });
    });

    document.querySelectorAll('[data-font-set]').forEach(btn => {
      btn.addEventListener('click', () => {
        window.JvmReader.setFont(btn.getAttribute('data-font-set'));
      });
    });

    document.querySelectorAll('[data-size-btn]').forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.getAttribute('data-size-btn');
        window.JvmReader.cycleSize(action);
      });
    });

    document.querySelectorAll('[data-width-toggle]').forEach(btn => {
      btn.addEventListener('click', () => {
        window.JvmReader.toggleWidth();
      });
    });

    // Mark as complete button on chapter
    const completeBtn = document.querySelector('.btn-mark-complete');
    if (completeBtn) {
      const currentModuleId = completeBtn.getAttribute('data-module');
      if (currentModuleId) {
        updateCompleteButtonState(currentModuleId);
        completeBtn.addEventListener('click', () => {
          window.JvmReader.toggleCompleted(currentModuleId);
        });
      }
    }
  }

  // Run immediately to prevent flash of wrong theme
  applySettings();

  // Run DOM enhancements on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      applySettings();
      setupToolbarControls();
      setupCodeBlocks();
      setupReadingProgress();
      setupKnowledgeChecks();
      updateSidebarProgress();
    });
  } else {
    applySettings();
    setupToolbarControls();
    setupCodeBlocks();
    setupReadingProgress();
    setupKnowledgeChecks();
    updateSidebarProgress();
  }
})();
