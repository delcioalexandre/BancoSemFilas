// Horários ocupados
const horariosOcupados = ["09:00", "11:00"];


// Seleciona formulário
const formulario = document.querySelector("form");


// Seleciona campo horário
const horario = document.querySelector("#horario");


// Seleciona área da senha
const senhaTexto = document.querySelector("#senha-gerada");


// Contador da senha
let contador = 1;


// Evento de envio
formulario.addEventListener("submit", function(event){

    // Impede atualização
    event.preventDefault();


    // Verifica se horário está ocupado
    if(horariosOcupados.includes(horario.value)){

        senhaTexto.innerHTML = "Horário indisponível!";

        senhaTexto.style.color = "red";

        return;
    }


    // Gera senha
    let senha = "A" + String(contador).padStart(3, "0");


    // Mostra senha
    senhaTexto.innerHTML =
    "Marcação confirmada! Sua senha é: " + senha;


    senhaTexto.style.color = "green";


    // Incrementa senha
    contador++;

});