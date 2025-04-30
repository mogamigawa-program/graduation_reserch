// ドロップダウンを開いたり閉じたりするスクリプト
document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('dropdownButton');
    const content = document.getElementById('dropdownContent');

    button.addEventListener('click', function() {
        content.classList.toggle('show');
    });

    // 外をクリックしたら閉じる
    window.addEventListener('click', function(e) {
        if (!button.contains(e.target)) {
            content.classList.remove('show');
        }
    });
});