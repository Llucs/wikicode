---
title: Patrón del Conmutador de Circuito en el Diseño del Sistema
description: Un mecanismo utilizado para prevenir que las fallas en una parte de un sistema distribuido propaguense a otras partes, mejorando la confiabilidad y estabilidad general del sistema.
created: 2026-07-06
tags:
  - diseño del sistema
  - microservicios
  - resiliencia
  - tolerancia a fallos
status: borrador
---

# Patrón del Conmutador de Circuito en el Diseño del Sistema

El Patrón del Conmutador de Circuito es un patrón de diseño utilizado en la ingeniería de software para prevenir las fallas en cascada en sistemas distribuidos. Funciona como un mecanismo de control que monitorea el éxito o la falla de operaciones remotas y cambia el comportamiento del sistema cuando las fallas superan un umbral específico. Cuando el conmutador de circuito está "abierto", detiene las solicitudes adicionales de llegar al servicio downstream, devolviendo una respuesta predeterminada al cliente en su lugar. Una vez que el servicio vuelve a un estado estable, el conmutador de circuito puede ser "cerrado" nuevamente, permitiendo que el sistema intente la operación de nuevo.

## Características Clave

1. **Detección de Disponibilidad del Servicio**: El conmutador de circuito monitorea el estado de servicios dependientes o componentes. Si un número determinado de fallas ocurren dentro de un intervalo específico de tiempo, el conmutador de circuito se activa.
2. **Mecanismo de Retroceso**: Cuando el conmutador de circuito está abierto, proporciona un mecanismo de retroceso que devuelve una respuesta predeterminada al cliente, evitando el fracaso total de la aplicación.
3. **Reintento Delatado**: En lugar de reintentar solicitudes fallidas inmediatamente, el conmutador de circuito permite un retraso, lo que puede ayudar al sistema a recuperarse de problemas transitorios.
4. **Estado del Conmutador de Circuito**: El conmutador de circuito mantiene un estado (abierto/cerrado) y transita entre estos estados basándose en el éxito o la falla del servicio.

## Instalación y Configuración

La implementación específica del Patrón del Conmutador de Circuito puede variar dependiendo del lenguaje de programación y el marco utilizado. Aquí hay un ejemplo básico usando una biblioteca Java popular llamada Hystrix.

### Agregar Dependencia

Para Maven, incluya la biblioteca Hystrix en su proyecto:

```xml
<dependency>
    <groupId>com.netflix.hystrix</groupId>
    <artifactId>hystrix-javanica</artifactId>
    <version>1.5.18</version>
</dependency>
```

### Crear un Comando

Defina un comando Hystrix para el servicio que desea proteger.

```java
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

public class MyServiceCommand extends HystrixCommand<String> {
    public MyServiceCommand() {
        super(HystrixCommandGroupKey.Factory.asKey("MyServiceGroup"));
    }

    @Override
    protected String run() throws Exception {
        // Llamar al servicio o operación aquí
        return callService();
    }

    @Override
    protected String getFallback() {
        return "Respuesta de retroceso";
    }
}
```

### Ejecutar el Comando

Use el comando para ejecutar la llamada al servicio.

```java
MyServiceCommand command = new MyServiceCommand();
String result = command.execute();
```

## Uso Básico

1. **Inicialización**: Cree una instancia del comando Hystrix.
2. **Ejecución**: Use el método `execute` para ejecutar el comando. Si el servicio no está disponible, se invoca el método de retroceso.
3. **Método de Retroceso**: Defina un método de retroceso que devuelva una respuesta predeterminada.

```java
@Override
protected String run() throws Exception {
    // Llamar al servicio o operación aquí
    return callService();
}

@Override
protected String getFallback() {
    return "Respuesta de retroceso";
}
```

4. **Monitorización**: Use Hystrix Dashboard para monitorear las estadísticas de ejecución y la salud de sus comandos.

## Casos de Uso

1. **Comunicación de Microservicios**: En arquitecturas de microservicios, donde los servicios se comunican entre sí, el Patrón del Conmutador de Circuito previene que una falla en un servicio propaguese a otros servicios.
2. **Puerta de Enlace de API**: Cuando una puerta de enlace de API gestiona el acceso a múltiples servicios, el Patrón del Conmutador evita que una falla en un servicio afecte toda la API.
3. **Servicios Terceros**: Al integrarse con servicios o API externos, el Patrón del Conmutador de Circuito ayuda a manejar las fallas transitorias de manera grácil.
4. **Acceso a la Base de Datos**: En interacciones con la base de datos, el patrón puede prevenir fallas debido a problemas temporales de conexión o sobrecarga de la base de datos.

## Conclusión

El Patrón del Conmutador de Circuito es una herramienta poderosa para gestionar las fallas en sistemas distribuidos, asegurando que las fallas en una parte del sistema no hundan al sistema entero. Al implementar este patrón, los desarrolladores pueden construir aplicaciones más resistentes y escalables.

---