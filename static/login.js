document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    const saved = JSON.parse(localStorage.getItem('savedAccounts') || '[]');

    if (saved.length === 0) {
        alert('Belum ada akun. Silakan sign up.');
        window.location.href = 'signup.html';
        return;
    }

    const valid = saved.some(line => {
        const [username, pass] = line.split(':');
        return username && pass && email === username.trim() && password === pass.trim();
    });

    if (valid) {
        window.location.href = 'index.html';
    } else {
        if (confirm('Login gagal! Daftar sekarang?')) {
            window.location.href = 'signup.html';
        }
    }
});