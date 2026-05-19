// Seleciona o formulário
const formulario = document.querySelector("form");


// Escuta o envio do formulário
formulario.addEventListener("submit", function(event){

    // Impede recarregamento automático da página
    event.preventDefault();


    // Seleciona todos os inputs
    const inputs = document.querySelectorAll("input");


    // Seleciona o campo select
    const select = document.querySelector("select");


    // Variável para verificar campos vazios
    let vazio = false;


    // Percorre todos os inputs
    inputs.forEach(function(input){

        // Verifica se input está vazio
        if(input.value === ""){

            vazio = true;

        }

    });


    // Verifica se serviço foi escolhido
    if(select.value === "Escolha o Serviço"){

        vazio = true;

    }


    // Verifica resultado final
    if(vazio){

        alert("Preencha todos os campos!");

    }else{

        alert("Marcação realizada com sucesso!");

    }

});