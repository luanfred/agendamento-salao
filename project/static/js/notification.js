function showToast(message, type) {
    if (type === "success") {
        color = "#2ECC71"; // Verde
    } else if (type === "error") {
        color = "#E74C3C"; // Vermelho
    }
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top", // Posição: 'top' ou 'bottom'
        position: "center", // 'left', 'center' ou 'right'
        backgroundColor: color, // Cor cinza escuro
        close: true, // Exibir botão de fechar
    }).showToast();
}