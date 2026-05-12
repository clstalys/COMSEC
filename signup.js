document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert('Password tidak cocok!');
        return;
    }

    if (password.length < 6) {
        alert('Password minimal 6 karakter!');
        return;
    }

    const saved = JSON.parse(localStorage.getItem('savedAccounts') || '[]');

    if (saved.some(line => line.split(':')[0].trim() === email)) {
        alert('Email sudah terdaftar!');
        return;
    }

    const updatedAccounts = [...saved, `${email}:${password}`];
    localStorage.setItem('savedAccounts', JSON.stringify(updatedAccounts));

    alert('Akun berhasil dibuat.');
    window.location.href = 'login.html';
});