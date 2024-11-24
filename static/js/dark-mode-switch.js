(function () {
  // Obtenemos la referencia al elemento de conmutación del tema con el ID "darkSwitch"
  var darkSwitch = document.getElementById("darkSwitch");

  if (darkSwitch) {
    // Llamamos a la función para inicializar el tema
    initTheme();

    // Agregamos un evento de cambio al elemento de conmutación del tema
    darkSwitch.addEventListener("change", function (event) {
      // Llamamos a la función para restablecer el tema
      resetTheme();
    });

    // Función para inicializar el tema
    function initTheme() {
      // Verificamos si la preferencia de tema oscuro está almacenada en el almacenamiento local
      var darkThemeSelected =
        localStorage.getItem("darkSwitch") !== null &&
        localStorage.getItem("darkSwitch") === "dark";
      // Establecemos el estado del interruptor según la preferencia
      darkSwitch.checked = darkThemeSelected;
      // Si se seleccionó el tema oscuro, establecemos el atributo "data-theme" en "dark" en el body
      if (darkThemeSelected) {
        document.body.setAttribute("data-theme", "dark");
      } else {
        // Si no se seleccionó el tema oscuro, eliminamos el atributo "data-theme" del body
        document.body.removeAttribute("data-theme");
      }
    }

    // Función para restablecer el tema
    function resetTheme() {
      if (darkSwitch.checked) {
        // Si se activa la conmutación del tema oscuro, establecemos el atributo "data-theme" en "dark" en el body
        document.body.setAttribute("data-theme", "dark");
        // Almacenamos la preferencia de tema oscuro en el almacenamiento local
        localStorage.setItem("darkSwitch", "dark");
      } else {
        // Si se desactiva la conmutación del tema oscuro, eliminamos el atributo "data-theme" del body
        document.body.removeAttribute("data-theme");
        // Eliminamos la preferencia de tema oscuro del almacenamiento local
        localStorage.removeItem("darkSwitch");
      }
    }
  }
})();
