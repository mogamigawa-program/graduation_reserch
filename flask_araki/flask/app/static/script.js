document.addEventListener('DOMContentLoaded', function () {
    // テーブル名の選択と送信ボタンの制御
    const tableSelect = document.getElementById('table_name');
    const submitButton = document.querySelector('button[type="submit"]');

    tableSelect.addEventListener('change', function () {
        if (tableSelect.value) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    });

    submitButton.disabled = !tableSelect.value;

    
});

