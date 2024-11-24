from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configura el controlador para Chrome
driver = webdriver.Chrome()

# URL de la página de inicio de sesión
driver.get("http://127.0.0.1:8000/tecnico/")

# Tiempo de espera explícita
wait = WebDriverWait(driver, 10)

# Paso 1: Iniciar sesión
try:
    # Espera a que el campo de correo electrónico esté interactivo y visible
    email_element = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    driver.execute_script("arguments[0].scrollIntoView();", email_element)
    email_element.send_keys("JUANITOGAMER@GMAIL.COM")

    # Espera a que el campo de contraseña esté interactivo y visible
    password_element = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    driver.execute_script("arguments[0].scrollIntoView();", password_element)
    password_element.send_keys("Sapito321=@")

    # Clic en el botón de inicio de sesión
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    # Esperar a que la redirección ocurra después del inicio de sesión
    wait.until(EC.url_changes("http://127.0.0.1:8000/tecnico/"))
    print("Inicio de sesión exitoso.")
except Exception as e:
    print("Error durante el inicio de sesión:", e)
    driver.quit()
    exit()

# Paso 2: Navegar a la página de creación de publicaciones
driver.get("http://127.0.0.1:8000/post/gestionar_publicaciones/")

# Paso 3: Medir el tiempo de carga del formulario
start_load = time.time()
try:
    # Espera a que el campo 'id_titulo' esté visible y habilitado para la interacción
    titulo_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "id_titulo"))
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_titulo"))
    )
    end_load = time.time()
    load_time = end_load - start_load
    print(f"Formulario cargado en {load_time:.2f} segundos.")
except Exception as e:
    print("Error al cargar el formulario:", e)
    driver.quit()
    exit()

# Verificar que el tiempo de carga sea menor a 3 segundos
if load_time >= 3:
    print(f"Advertencia: El formulario tardó en cargar {load_time:.2f} segundos.")

# Paso 4: Completar y enviar el formulario
# Paso 4: Completar y enviar el formulario
submit_time = None  # Inicializar submit_time

try:
    # Completar los campos del formulario
    driver.find_element(By.ID, "id_titulo").send_keys("Título de prueba")
    driver.find_element(By.ID, "id_descripcion").send_keys("Descripción de prueba")
    driver.find_element(By.ID, "id_limite_monto").send_keys("1000")

    # Deja el campo de imagen vacío

    driver.find_element(By.ID, "id_ubicacion").send_keys("Ubicación de prueba")

    # Medir el tiempo de envío
    start_submit = time.time()

    # Enviar el formulario
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit_button")))
    submit_button.click()

    # Esperar que el mensaje de éxito aparezca (basado en el HTML proporcionado)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "messages")))  # Espera a que aparezca la lista de mensajes
    # También podrías esperar que un mensaje específico esté presente dentro de la lista
    # wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='messages']//li[contains(text(),'Formulario enviado')]")))

    end_submit = time.time()
    submit_time = end_submit - start_submit
    print(f"Formulario enviado y notificación recibida en {submit_time:.2f} segundos.")
except Exception as e:
    print("Ocurrió un error durante la prueba:", e)

# Verificar que el tiempo de envío sea menor a 2 segundos solo si se definió submit_time
if submit_time is not None:
    if submit_time >= 2:
        print(f"Advertencia: El envío tardó en procesarse {submit_time:.2f} segundos.")
    else:
        print("El envío se procesó dentro del tiempo esperado.")
else:
    print("El tiempo de envío no fue medido debido a un error durante el envío del formulario.")

# Cerrar el navegador al finalizar la prueba
driver.quit()
