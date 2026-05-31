// home page
// mobile nav
function toggleMobileNav() { document.getElementById('mobile-nav').classList.toggle('open'); }
function closeMobileNav() { document.getElementById('mobile-nav').classList.remove('open'); }
document.addEventListener('click', function(e) {
const nav = document.getElementById('mobile-nav');
const btn = document.querySelector('.ham-btn');
if (nav && btn && !nav.contains(e.target) && !btn.contains(e.target)) nav.classList.remove('open');
});

// Tabs
function switchTab(id, btn) {
document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
document.getElementById('panel-' + id).classList.add('active');
if (btn) {
    btn.classList.add('active');
} else {
    document.querySelectorAll('.tab-btn').forEach(b => {
    if ((id === 'home' && b.textContent.includes('Home')) ||
        (id === 'about' && b.textContent.includes('About'))) {
        b.classList.add('active');
    }
    });
}
window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Switch tab then scroll to a specific card
function switchTabTo(id, anchorId) {
switchTab(id, null);
setTimeout(() => {
    const el = document.getElementById(anchorId);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}, 120);
}

// Inline read more
function toggleStory() {
const rest = document.getElementById('storyRest');
const dots = document.getElementById('storyDots');
const isOpen = rest.classList.contains('open');
rest.classList.toggle('open');
dots.style.display = isOpen ? 'inline' : 'none';
}

// Back to top
window.addEventListener('scroll', () => {
document.getElementById('back-top').classList.toggle('visible', window.scrollY > 300);
});

// Stop blink on click
document.querySelectorAll('.nav-blink').forEach(link => {
link.addEventListener('click', () => link.classList.remove('nav-blink'));
});



// reoprt and finding page
// MOBILE NAV
// Stop blink on click (optional UX improvement)

// TABS
function switchTabReport(name, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('panel-' + name).classList.add('active');
  const sidebar  = document.getElementById('sidebar-toc');
  const pageWrap = document.getElementById('page-wrap');
  if (name === 'report') {
    sidebar.style.display = '';
    pageWrap.classList.remove('no-sidebar');
  } else {
    sidebar.style.display = 'none';
    pageWrap.classList.add('no-sidebar');
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// COUNTERS
function animCount(id, target, dur, suffix) {
  const el = document.getElementById(id);
  if (!el) return;
  let s = null;
  function step(ts) {
    if (!s) s = ts;
    const p = Math.min((ts - s) / dur, 1);
    const e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(e * target) + (suffix || '');
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    animCount('s1', 111, 1200, '');
    animCount('s2', 6,   800,  '');
    animCount('s3', 4,   700,  '');
    animCount('s4', 84,  1000, '%');
  }
}, { threshold: 0.3 }).observe(document.querySelector('.stat-strip'));

// CHARTS
Chart.defaults.font.family = "'Segoe UI', sans-serif";
Chart.defaults.color = '#e8e4f0';

new Chart(document.getElementById('bankChart'), {
  type: 'bar',
  data: {
    labels: ['Bank of Bhutan', 'DK Bank', 'Bhutan National Bank', 'Druk PNB', 'T Bank', 'BDBL'],
    datasets: [{ label: 'Preference (%)', data: [84.47,7.77,4.85,1.94,0.97,0],
      backgroundColor: ['#8b6801','#8e7015','#ae8d2b','#c9a845','#c7ac5d','#c8b270'],
      borderColor: '#c1981c', borderWidth: 1, borderRadius: 6 }]
  },
  options: { responsive: true, plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, max: 100, grid: { color: 'rgba(212,168,32,0.15)' }, ticks: { callback: v => v+'%', color: '#e8e4f0' } }, x: { grid: { display: false }, ticks: { color: '#e8e4f0' } } } }
});

new Chart(document.getElementById('switchChart'), {
  type: 'doughnut',
  data: {
    labels: ['Very unlikely','Unlikely','Unsure','Likely','Very likely'],
    datasets: [{ data: [6.80,22.33,31.07,29.13,10.69],
      backgroundColor: ['rgba(16,146,2,0.6)','rgba(53,181,39,0.95)','rgba(99,173,3,0.95)','rgba(126,220,4,0.95)','rgba(184,252,95,0.95)'],
      borderWidth: 0, hoverOffset: 6 }]
  },
  options: { responsive: true, cutout: '62%', plugins: { legend: { position:'right', labels: { padding:16, font:{size:11}, color:'#e8e4f0' } } } }
});

new Chart(document.getElementById('accountChart'), {
  type: 'pie',
  data: {
    labels: ['Have a bank account','Do not have an account'],
    datasets: [{ data: [103,8],
      backgroundColor: ['rgba(249,28,3,0.8)','rgba(254,202,43,0.6)'],
      borderWidth: 0, hoverOffset: 6 }]
  },
  options: { responsive: true, plugins: { legend: { position:'right', labels: { padding:16, font:{size:11}, color:'#e8e4f0' } } } }
});

// BACK TO TOP

// TOC ACTIVE
const tocLinks = document.querySelectorAll('.toc a');
document.querySelectorAll('.rs, .stat-strip').forEach(el => {
  if (!el.id) return;
  new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        tocLinks.forEach(a => a.classList.remove('active'));
        const m = document.querySelector(`.toc a[href="#${e.target.id}"]`);
        if (m) m.classList.add('active');
      }
    });
  }, { threshold: 0.4 }).observe(el);
});




// prototype page


// Story modal
function openStoryModal() {
  const overlay = document.getElementById('storyModal');
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
  // Reset scroll n progress
  const body = document.getElementById('modalBody');
  body.scrollTop = 0;
  updateProgress();
}

function closeStoryModal() {
  const overlay = document.getElementById('storyModal');
  overlay.classList.remove('open');
  document.body.style.overflow = '';
}

function handleOverlayClick(e) {
  if (e.target === document.getElementById('storyModal')) closeStoryModal();
}

function updateProgress() {
  const body = document.getElementById('modalBody');
  const fill = document.getElementById('progressFill');
  const pct = document.getElementById('progressPct');
  const scrolled = body.scrollTop;
  const total = body.scrollHeight - body.clientHeight;
  const progress = total > 0 ? Math.min(100, Math.round((scrolled / total) * 100)) : 0;
  fill.style.width = progress + '%';
  pct.textContent = progress + '%';
}

// Close on Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeStoryModal();
});



// finsight page 

// Stop blink on click (optional UX improvement)



// contact page
// MOBILE NAV
// Stop blink on click

document.addEventListener('DOMContentLoaded', function () {

  // EMAILJS INIT
  emailjs.init('f49nkV21mfm4epoil');
  const EMAILJS_SERVICE_ID = 'service_mf5ec4b';

  // STATE
  let selectedPurpose = '';

  // CHIP SELECTION
  function selectChip(value, btn) {
    document.querySelectorAll('.form-chip').forEach(c => c.classList.remove('sel'));
    btn.classList.add('sel');
    selectedPurpose = value;
    document.getElementById('purpose').value = value;
  }

  // CHIP SELECTION - left sidebar
  function pickPurpose(value, btn) {
    document.querySelectorAll('.chip').forEach(c => c.classList.remove('selected'));
    btn.classList.add('selected');
    document.querySelectorAll('.form-chip').forEach(c => {
      if (c.getAttribute('onclick').includes(`'${value}'`)) {
        c.classList.add('sel');
      } else {
        c.classList.remove('sel');
      }
    });
    selectedPurpose = value;
    document.getElementById('purpose').value = value;
    document.querySelector('.form-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // CHAR COUNT
  function updateCount() {
    document.getElementById('char-count').textContent =
      document.getElementById('message').value.length;
  }

  // FIELD HIGHLIGHT
  function highlight(id) {
    const el = document.getElementById(id);
    el.style.borderColor = 'rgba(192,57,43,0.8)';
    el.style.boxShadow = '0 0 0 3px rgba(192,57,43,0.15)';
    setTimeout(() => { el.style.borderColor = ''; el.style.boxShadow = ''; }, 2500);
  }

  // ALERT
  function showAlert(type, msg) {
    document.getElementById('alert-success').classList.remove('show');
    document.getElementById('alert-error').classList.remove('show');
    if (type === 'success') {
      document.getElementById('alert-success').classList.add('show');
    } else {
      document.getElementById('error-text').textContent =
        msg || 'Something went wrong. Please try again.';
      document.getElementById('alert-error').classList.add('show');
    }
  }

  // SUBMIT
  async function handleSubmit() {
    const fname   = document.getElementById('fname').value.trim();
    const lname   = document.getElementById('lname').value.trim();
    const email   = document.getElementById('email').value.trim();
    const phone   = document.getElementById('phone').value.trim();
    const message = document.getElementById('message').value.trim();

    document.getElementById('alert-success').classList.remove('show');
    document.getElementById('alert-error').classList.remove('show');

    let valid = true;
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      highlight('email'); valid = false;
    }
    if (!selectedPurpose) {
      showAlert('error', 'Please select a purpose for your message.');
      valid = false;
    }
    if (!message) { highlight('message'); valid = false; }
    if (!valid) return;

    const btn = document.getElementById('submit-btn');
    btn.disabled = true;
    document.getElementById('btn-text').textContent = 'Sending…';
    document.getElementById('spinner').style.display = 'block';

    const templateParams = {
      // from_name: (fname || lname) ? [fname, lname].filter(Boolean).join(' ') : 'Anonymous',
      from_name: fname || lname || 'there',
      from_email: email,
      phone:      phone || 'Not provided',
      purpose:    selectedPurpose,
      message:    message,
      to_email:   'hemaluitel5@gmail.com',
      to_name:    fname || 'there',    
      reply_to:   email,
    };

    try {
      await emailjs.send(EMAILJS_SERVICE_ID, 'template_8n9vvxb', templateParams);
      await emailjs.send(EMAILJS_SERVICE_ID, 'template_6ktwkzm', templateParams);

      showAlert('success');
      ['fname','lname','email','phone','message']
        .forEach(id => document.getElementById(id).value = '');
      document.querySelectorAll('.form-chip, .chip')
        .forEach(c => c.classList.remove('sel','selected'));
      selectedPurpose = '';
      document.getElementById('purpose').value = '';
      document.getElementById('char-count').textContent = '0';

    } catch (err) {
      console.error('EmailJS error:', err);
      showAlert('error', 'Failed to send. Please email hemaluitel5@gmail.com directly.');
    } finally {
      btn.disabled = false;
      document.getElementById('btn-text').textContent = 'Send message';
      document.getElementById('spinner').style.display = 'none';
    }
  }

  // EXPOSE to onclick attributes in HTML
  window.selectChip   = selectChip;
  window.pickPurpose  = pickPurpose;
  window.updateCount  = updateCount;
  window.handleSubmit = handleSubmit;

}); // end DOMContentLoaded
