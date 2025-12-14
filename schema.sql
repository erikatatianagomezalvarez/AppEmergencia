-- ============================================================
-- Schema para AppEmergencia
-- Crea todas las tablas necesarias con relaciones correctas
-- ============================================================

-- Tabla de usuarios (PARENT)
CREATE TABLE IF NOT EXISTS tbusuario (
  idUsuario INT AUTO_INCREMENT PRIMARY KEY,
  cedulaUsuario VARCHAR(20),
  nombresApellidosUsuario VARCHAR(200),
  telefonoUsuario VARCHAR(50),
  contactoEmergenciaUsuario VARCHAR(50),
  tipoUsuario VARCHAR(50),
  direccionUsuario VARCHAR(255),
  emailUsuario VARCHAR(150),
  fechaRegistroUsuario DATETIME,
  estadoUsuario VARCHAR(20)
);

-- Tabla de tipos de emergencia (PARENT)
CREATE TABLE IF NOT EXISTS tbtipoemergencia (
  idTipoEmergencia INT AUTO_INCREMENT PRIMARY KEY,
  nombreTipoEmergencia VARCHAR(50) NOT NULL,
  descripcionTipoEmergencia TEXT,
  nivelPrioridadTipoEmergencia_3 ENUM('baja','media','alta','critica') NOT NULL,
  estadoTipoEmergencia_4 ENUM('activo','inactivo') NOT NULL
);

-- Tabla de servicios de emergencia
CREATE TABLE IF NOT EXISTS tbservicioemergencia (
  idServicioEmergencia INT AUTO_INCREMENT PRIMARY KEY,
  nombreServicioEmergencia VARCHAR(100),
  tipoServicioEmergencia VARCHAR(50),
  telefonoServicioEmergencia VARCHAR(20),
  disponibilidadServicioEmergencia VARCHAR(50),
  direccionServicioEmergencia VARCHAR(255),
  capacidadServicioEmergencia INT,
  horarioServicioEmergencia VARCHAR(100),
  especialidadServicioEmergencia VARCHAR(100),
  estadoServicioEmergencia VARCHAR(20)
);

-- Tabla de contactos de emergencia
CREATE TABLE IF NOT EXISTS tbcontactoemergencia (
  idContactoEmergencia INT AUTO_INCREMENT PRIMARY KEY,
  tbTipoEmergencia_idTipoEmergencia INT NOT NULL,
  nombreContactoEmergencia VARCHAR(100),
  telefonoContactoEmergencia VARCHAR(20),
  tipoContactoEmergencia VARCHAR(50),
  descripcionContactoEmergencia TEXT,
  estadoContactoEmergencia VARCHAR(20),
  FOREIGN KEY (tbTipoEmergencia_idTipoEmergencia) REFERENCES tbtipoemergencia(idTipoEmergencia)
);

-- Tabla de emergencias (CHILD: referencias a tbusuario y tbtipoemergencia)
CREATE TABLE IF NOT EXISTS tbemergencia (
  idEmergencia INT AUTO_INCREMENT PRIMARY KEY,
  tbUsuario_idUsuario INT NOT NULL,
  tbTipoEmergencia_idTipoEmergencia INT NOT NULL,
  codigoEmergencia INT,
  fechaHoraEmergencia DATETIME,
  tipoEmergencia INT,
  estadoEmergencia ENUM('reportada','en_proceso','atendida','cerrada'),
  ubicacionEmergencia VARCHAR(300),
  latitudEmergencia DECIMAL(11,8),
  longitudEmergencia DECIMAL(11,8),
  descripcionEmergencia TEXT,
  prioridadEmergencia ENUM('baja','media','alta','critica'),
  idusuarioreportaEmergencia INT,
  fechaCierreEmergencia DATETIME,
  observacionesEmergencia TEXT,
  FOREIGN KEY (tbUsuario_idUsuario) REFERENCES tbusuario(idUsuario) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (tbTipoEmergencia_idTipoEmergencia) REFERENCES tbtipoemergencia(idTipoEmergencia) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla de historial de estados
CREATE TABLE IF NOT EXISTS tbhistorialestados (
  idHistorialEstados INT AUTO_INCREMENT PRIMARY KEY,
  tbEmergencia_idEmergencia INT NOT NULL,
  tbUsuario_idUsuario INT NOT NULL,
  estadoAnterior VARCHAR(50),
  estadoNuevo VARCHAR(50),
  fechaCambioHistorialEstados DATETIME,
  usuarioCambioHistorialEstados VARCHAR(100),
  motivoHistorialEstados TEXT,
  FOREIGN KEY (tbEmergencia_idEmergencia) REFERENCES tbemergencia(idEmergencia) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (tbUsuario_idUsuario) REFERENCES tbusuario(idUsuario) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla de despachos
CREATE TABLE IF NOT EXISTS tbdespacho (
  idDespacho INT AUTO_INCREMENT PRIMARY KEY,
  tbServicioEmergencia_idServicioEmergencia INT NOT NULL,
  tbEmergencia_idEmergencia INT NOT NULL,
  idServicio INT,
  horaAsignacionDespacho DATETIME,
  horaLlegadaDespacho DATETIME,
  horaFinalizacionDespacho DATETIME,
  estadoDespacho ENUM('asignado','en_ruta','en_sitio','finalizado'),
  observacionesDespacho TEXT,
  tiempoRespuestaDespacho INT,
  calificacionDespacho INT,
  FOREIGN KEY (tbServicioEmergencia_idServicioEmergencia) REFERENCES tbservicioemergencia(idServicioEmergencia) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (tbEmergencia_idEmergencia) REFERENCES tbemergencia(idEmergencia) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Índices para mejorar búsquedas
CREATE INDEX idx_emergencia_usuario ON tbemergencia(tbUsuario_idUsuario);
CREATE INDEX idx_emergencia_tipo ON tbemergencia(tbTipoEmergencia_idTipoEmergencia);
CREATE INDEX idx_emergencia_estado ON tbemergencia(estadoEmergencia);
CREATE INDEX idx_contacto_tipo ON tbcontactoemergencia(tbTipoEmergencia_idTipoEmergencia);
CREATE INDEX idx_historial_emergencia ON tbhistorialestados(tbEmergencia_idEmergencia);
CREATE INDEX idx_historial_usuario ON tbhistorialestados(tbUsuario_idUsuario);
CREATE INDEX idx_despacho_servicio ON tbdespacho(tbServicioEmergencia_idServicioEmergencia);
CREATE INDEX idx_despacho_emergencia ON tbdespacho(tbEmergencia_idEmergencia);
CREATE INDEX idx_despacho_estado ON tbdespacho(estadoDespacho);
