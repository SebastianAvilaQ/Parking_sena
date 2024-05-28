
function mostrarContrasena() {
  var passwordField = document.getElementById('password');
  var icon = document.getElementById('show-password-button');
  if (passwordField.type === "password") {
      passwordField.type = "text";
      icon.classList.add('visible-password');
  } else {
      passwordField.type = "password";
      icon.classList.remove('visible-password');
  }
}

  function validarFormularioUsuario() {
    var nombres = document.getElementById('nombresid').value;
    var correo = document.getElementById('correoElectronicoid').value;
    var tipoDoc = document.getElementById('TipoDocumentoid').value;
    var numDoc = document.getElementById('numeroDocumentoid').value;
  
    if (nombres === "") { 
      alert("Por favor, complete el campo de nombre.");
      // Evita que se envíe el formulario si la validación falla
      return false;
    }
  
    if (correo === "") {
      alert("Por favor, complete el campo de correo electrónico.");
      return false;
    }
  
    if (tipoDoc === "") {
      alert("Por favor, seleccione un tipo de documento.");
      return false;
    }
  
    if (numDoc === "") {
      alert("Por favor, complete el campo de número de documento.");
      return false; // Evita que se envíe el formulario si la validación falla
    }
  
    return true; // Permite que se envíe el formulario si la validación pasa
  }

  function validarFormularioVisitantes() {
    var nombresVis = document.getElementById('nombresVisitanteid').value;
    var apellidosVis = document.getElementById('apellidosVisitanteid').value;
    var cedulaVis = document.getElementById('cedulaid').value;
    if (nombresVis === "") { 
      alert("Por favor, complete el campo de nombre.");
      // Evita que se envíe el formulario si la validación falla
      return false;
    }
  
    if (apellidosVis === "") {
      alert("Por favor, complete el campo de Apellidos.");
      return false;
    }
  
    if (cedulaVis === "") {
      alert("Por favor, seleccione su cedula.");
      return false;
    }
    return true; // Permite que se envíe el formulario si la validación pasa
  }

  function validarFormularioVehiculo() {
    var cedulaVe = document.getElementById('cedulaDueñoid').value;
    var placave = document.getElementById('placaid').value;
    var tipove = document.getElementById('tipoid').value;
    if (cedulaVe === "") { 
      alert("Por favor, complete el campo de cedula.");
      // Evita que se envíe el formulario si la validación falla
      return false;
    }
  
    if (placave === "") {
      alert("Por favor, complete el campo de la placa.");
      return false;
    }
  
    if (tipove === "") {
      alert("Por favor, complete el tipo de vehiculo.");
      return false;
    }
    return true; // Permite que se envíe el formulario si la validación pasa
  }


  function validarFormularioArtefactosExternos() {
    var nombreArt = document.getElementById('nombreArtefactosExternosid').value;
    var DescripArt = document.getElementById('descripcionArtefactosExternosid').value;
    if (nombreArt === "") { 
      alert("Por favor, complete el nombre del artefacto.");
      // Evita que se envíe el formulario si la validación falla
      return false;
    }
  
    if (DescripArt === "") {
      alert("Por favor, complete el campo de la descripcion.");
      return false;
    }
    return true; // Permite que se envíe el formulario si la validación pasa
  }

  
  function validarFormulariosalidaVehi() {
    var placaEntraVe = document.getElementById('placasalidaid').value;
    var horaEntraVe = document.getElementById('horasalidaid').value;
    var fechaEntraVe = document.getElementById('fechasalidaid').value;
    if (placaEntraVe === "") { 
      alert("Por favor, complete la placa del vehiculo.");
      // Evita que se envíe el formulario si la validación falla
      return false;
    }
  
    if (horaEntraVe === "") {
      alert("Por favor, complete el campo de la hora de salida del vehiculo.");
      return false;
    }
    if (fechaEntraVe === "") {
      alert("Por favor, complete el campo de la fecha de salida del vehiculo.");
      return false;
    }
    return true; // Permite que se envíe el formulario si la validación pasa
  }

  function validarFormularioSalidaVeh() {
    var placaSalidaVeh = document.getElementById('placaSalidaid').value;
    var horaSalidaVeh = document.getElementById('horaSalidaid').value;
    var fechaSalidaVeh = document.getElementById('fechaSalidaid').value;
    if (placaSalidaVeh === "") { 
      alert("Por favor, complete la placa del vehiculo.");
      // Evita que se envíe el formulario si la validación falla
      return false;
    }
  
    if (horaSalidaVeh === "") {
      alert("Por favor, complete el campo de la hora de salida del vehiculo.");
      return false;
    }
    if (fechaSalidaVeh === "") {
      alert("Por favor, complete el campo de la fecha de salida del vehiculo.");
      return false;
    }
    return true; // Permite que se envíe el formulario si la validación pasa
  }

