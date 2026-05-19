// Número inicial
let contador = 1;


// Seleciona formulário
const formulario = document.querySelector("form");


// Seleciona área da senha
const senhaTexto = document.querySelector("#senha-gerada");


// Evento de envio
formulario.addEventListener("submit", function(event){

    // Impede atualização
    event.preventDefault();


    // Gera senha
    let senha = "A" + String(contador).padStart(3, "0");


    // Mostra senha na tela
    senhaTexto.innerHTML = "Sua senha é: " + senha;


    // Incrementa contador
    contador++;

});