const formulario = document.querySelector("form");

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    alert("Marcação realizada com sucesso!");

});