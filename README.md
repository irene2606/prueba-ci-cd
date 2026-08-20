# Prueba pipeline CI/CD

**Nota:** La aplicación (`app.py`) es un script muy sencillo porque la idea de esta práctica es centrarse en el funcionamiento del CI/CD y GitHub Actions.

Este repo es una práctica de CI/CD. El pipeline primero comprueba si el código funciona bien mediante tests, si es así, construye y sube la imagen Docker al Registry, evitando subir a producción código que está roto.

## Organización del pipeline

Hay dos workflows separados, uno para CI y otro para CD:

1. **CI (Integración Continua)**
   * Se lanza con cada `push` o `pull_request` a `main`.
   * Qué hace:
     * Revisa el estilo del código con Flake8.
     * Ejecuta los tests con Pytest.
     * Levanta una base de datos PostgreSQL de prueba (temporal, solo para el pipeline) y comprueba que el script `insertar_sensor.py` inserta datos correctamente.

2. **CD (Entrega Continua / Release)**
   * Este solo se lanza cuando el CI ha terminado bien.
   * Qué hace:
     * Hace login en Docker Hub.
     * Construye la imagen con `docker build`.
     * La sube a Docker Hub con `docker push` (tag `latest`).

---

## Secrets necesarios

Por seguridad, las credenciales y datos sensibles no se guardan directamente en el código ni en los archivos de configuración. Se han añadido como Secrets del repositorio:

| Secreto | Para qué es |
| :--- | :--- |
| `DB_NAME` | Nombre de la BD de Postgres para los tests |
| `DB_USER` | Usuario de Postgres |
| `DB_PASSWORD` | Contraseña de Postgres |
| `DOCKER_USERNAME` | Usuario de Docker Hub |
| `DOCKER_PASSWORD` | Access Token de Docker Hub (con permisos de lectura/escritura) |

---

## Cómo probar la imagen

La imagen es pública en Docker Hub, así que se puede bajar y probar en cualquier sitio con Docker instalado:

```bash
# Descargar la última imagen
docker pull irene2606/motor-app:latest

# Ejecutar el contenedor
docker run irene2606/motor-app:latest
```
