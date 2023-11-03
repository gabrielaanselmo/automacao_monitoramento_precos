function gerarPrecoAleatorio(min, max) {
  return (Math.random() * (max - min) + min).toFixed(2);
}

function atualizarPreco() {
  var novoPreco = gerarPrecoAleatorio(10, 100);
  document.getElementById('product-price').textContent = novoPreco;
}

setInterval(atualizarPreco, 5000);
document.addEventListener('DOMContentLoaded', atualizarPreco);
