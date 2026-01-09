# Módulo Odoo: Gestión Hospitalaria

Este proyecto contiene un módulo personalizado para Odoo 18 que implementa un sistema completo de gestión hospitalaria, desplegado mediante Docker.

---

## Descripción General

El proyecto incluye el módulo principal:

### **módulo_hospital**
Sistema completo de gestión hospitalaria que permite administrar pacientes, médicos y diagnósticos con relaciones complejas entre entidades.

---

## Estructura del Proyecto

```
Tarea_18_ModuloRelaciones_Hospital/
├── docker-compose.yml           # Configuración de Docker para la aplicación
├── config/
│   └── odoo.conf               # Configuración de Odoo
├── extra-addons/
│   └── modulo_hospital/        # Módulo de gestión hospitalaria
│       ├── __init__.py
│       ├── __manifest__.py     # Metadatos del módulo
│       ├── controllers/
│       │   └── controllers.py
│       ├── demo/
│       │   └── demo.xml        # Datos de demostración
│       ├── models/
│       │   ├── __init__.py
│       │   ├── paciente.py     # Modelo de Paciente
│       │   ├── medico.py       # Modelo de Médico
│       │   ├── diagnostico.py  # Modelo de Diagnóstico
│       │   └── models.py
│       ├── security/
│       │   └── ir.model.access.csv  # Control de acceso
│       └── views/
│           ├── paciente_hospital_views.xml
│           ├── medico_hospital_views.xml
│           ├── diagnostico_hospital_views.xml
│           ├── menu.xml
│           ├── templates.xml
│           └── views.xml
```

---

## Módulo Hospital: Gestión Hospitalaria

### Descripción
Módulo especializado en la gestión de la interacción entre pacientes y médicos, registrando los diagnósticos y consultas realizadas.

### Modelos de Datos

#### **Paciente** (`modulo_hospital.paciente`)
Representa a un paciente del hospital.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_paciente` | Char | ID único del paciente (requerido) |
| `nombre` | Char | Nombre del paciente (requerido) |
| `apellidos` | Char | Apellidos del paciente (requerido) |
| `sintomas` | Text | Descripción de síntomas presentados |
| `diagnostico_ids` | One2many | Relación con diagnósticos (Paciente → Diagnóstico) |
| `medico_ids` | Many2many | Médicos que han atendido al paciente (calculado) |

**Código del Modelo** (`paciente.py`):
```python
from odoo import models, fields

class Paciente(models.Model):
    _name = 'modulo_hospital.paciente'
    _description = 'Paciente'

    id_paciente = fields.Char(string = "ID Paciente", required = True)
    nombre = fields.Char(string = "Nombre", required = True)
    apellidos = fields.Char(string = "Apellidos", required = True)
    sintomas = fields.Text(string = "Síntomas")
    diagnostico_ids = fields.One2many('modulo_hospital.diagnostico', 'paciente_id', string = "Diagnósticos")
    medico_ids = fields.Many2many('modulo_hospital.medico', compute='_compute_medicos', string="Médicos que atendieron al paciente")

    def _compute_medicos(self):
        for paciente in self:
            paciente.medico_ids = paciente.diagnostico_ids.mapped('medico_id')
```

**Aspectos clave:**
- El campo `medico_ids` es calculado mediante la función `_compute_medicos()`, que extrae los médicos desde los diagnósticos asociados
- Utiliza `mapped()` para obtener los registros de médico desde los diagnósticos relacionados
- El modelo hereda de `models.Model` de Odoo

#### **Médico** (`modulo_hospital.medico`)
Representa a un profesional médico.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_medico` | Char | ID único del médico (requerido) |
| `nombre` | Char | Nombre del médico (requerido) |
| `apellidos` | Char | Apellidos del médico (requerido) |
| `numero_colegiado` | Char | Número de colegiación (requerido) |
| `consulta` | Text | Información sobre consultas |
| `diagnostico_ids` | One2many | Relación con diagnósticos (Médico → Diagnóstico) |
| `paciente_ids` | Many2many | Pacientes atendidos (calculado) |

**Código del Modelo** (`medico.py`):
```python
from odoo import models, fields

class Medico(models.Model):
    _name = 'modulo_hospital.medico'
    _description = 'Medico'

    id_medico = fields.Char(string = "ID Medico", required = True)
    nombre = fields.Char(string = "Nombre", required = True)
    apellidos = fields.Char(string = "Apellidos", required = True)
    numero_colegiado = fields.Char(string = "Nª colegiado", required = True)
    consulta = fields.Text(string = "Consultas")
    diagnostico_ids = fields.One2many('modulo_hospital.diagnostico', 'medico_id', string = "Diagnósticos")
    paciente_ids = fields.Many2many('modulo_hospital.paciente', compute = '_compute_pacientes', string = 'Pacientes atendidos por este medico')

    def _compute_pacientes(self):
        for medico in self:
            medico.paciente_ids = medico.diagnostico_ids.mapped('paciente_id')
```

**Aspectos clave:**
- Similar al modelo Paciente, utiliza un campo calculado `paciente_ids` para obtener los pacientes atendidos
- La función `_compute_pacientes()` extrae los pacientes desde los diagnósticos realizados
- Almacena la información del profesional médico (colegiación, etc.)

#### **Diagnóstico** (`modulo_hospital.diagnostico`)
Relación entre médico y paciente con información del diagnóstico.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `medico_id` | Many2one | Médico que realiza el diagnóstico (requerido) |
| `paciente_id` | Many2one | Paciente diagnosticado (requerido) |
| `sintoma` | Text | Síntomas del paciente (relacionado, solo lectura) |
| `consulta` | Text | Consulta del médico (relacionado, solo lectura) |

**Código del Modelo** (`diagnostico.py`):
```python
from odoo import models, fields

class Diagnostico(models.Model):
    _name = 'modulo_hospital.diagnostico'
    _description = 'Diagnósticos de los pacientes'

    medico_id = fields.Many2one('modulo_hospital.medico', string = 'Medico', required = True)
    paciente_id = fields.Many2one('modulo_hospital.paciente', string = 'Paciente', required = True)
    sintoma = fields.Text(related = 'paciente_id.sintomas', string = 'Sintomas', readonly = True)
    consulta = fields.Text(related = 'medico_id.consulta', string = 'Consultas', readonly = True)
```

**Aspectos clave:**
- Es el modelo de unión que conecta Médico y Paciente
- Utiliza campos `related` para mostrar información del médico y paciente de forma sincronizada
- Los campos relacionados son de solo lectura, reflejando los valores de los modelos relacionados
- Actúa como tabla intermedia en la relación Many2many entre Médico y Paciente

### Relaciones

- **Paciente ↔ Diagnóstico**: 1 a Muchos (Un paciente puede tener múltiples diagnósticos)
- **Médico ↔ Diagnóstico**: 1 a Muchos (Un médico puede realizar múltiples diagnósticos)
- **Paciente ↔ Médico**: Muchos a Muchos (A través de Diagnóstico)

### Vistas del Módulo Hospital

Las vistas están definidas en archivos XML y proporcionan la interfaz de usuario para interactuar con los modelos.

#### **Vistas de Paciente**

**Vista de Formulario (Pacientes atendidos)**
- **Archivo**: `paciente_hospital_views.xml`
- **ID**: `view_hospital_paciente_form`
- **Estructura**:
  - **Sección Principal**: Muestra los campos básicos del paciente
    - ID Paciente
    - Nombre
    - Apellidos
    - Síntomas
  - **Pestaña de Notebook**: "Médicos que atendieron al paciente"
    - Tabla de solo lectura mostrando:
      - Nombre del médico
      - Apellidos del médico
      - Consulta del médico

**Código XML**:
```xml
<record id="view_hospital_paciente_form" model="ir.ui.view">
    <field name="name">hospital.paciente.form</field>
    <field name="model">modulo_hospital.paciente</field>
    <field name="arch" type="xml">
        <form string = "Pacientes atendidos">
            <sheet>
                <group>
                    <field name = "id_paciente"/>
                    <field name = "nombre"/>
                    <field name = "apellidos"/>
                    <field name = "sintomas"/>
                </group>
                <notebook>
                    <page string = "Médicos que atendieron al paciente">
                        <field name = "medico_ids" readonly="1">
                            <list>
                                <field name = "nombre"/>
                                <field name = "apellidos"/>
                                <field name = "consulta"/>
                            </list>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

**Vista de Lista**
- **ID**: `view_hospital_paciente_list`
- **Columnas mostradas**:
  - ID Paciente
  - Nombre
  - Apellidos

**Código XML**:
```xml
<record id="view_hospital_paciente_list" model="ir.ui.view">
    <field name="name">hospital.paciente.list</field>
    <field name="model">modulo_hospital.paciente</field>
    <field name="arch" type="xml">
        <list>
            <field name="id_paciente"/>
            <field name="nombre"/>
            <field name="apellidos"/>
        </list>
    </field>
</record>
```

#### **Vistas de Médico**

**Vista de Formulario (Médicos)**
- **Archivo**: `medico_hospital_views.xml`
- **ID**: `view_hospital_medico_form`
- **Estructura**:
  - **Sección Principal**: Muestra los datos del profesional
    - ID Médico
    - Nombre
    - Apellidos
    - Número de colegiación
    - Consulta
  - **Pestaña de Notebook**: "Pacientes atendidos"
    - Tabla de solo lectura mostrando:
      - Nombre del paciente
      - Apellidos del paciente
      - Síntomas del paciente

**Código XML**:
```xml
<record id="view_hospital_medico_form" model="ir.ui.view">
    <field name="name">hospital.medico.form</field>
    <field name="model">modulo_hospital.medico</field>
    <field name="arch" type="xml">
        <form string = "Médicos">
            <sheet>
                <group>
                    <field name = "id_medico"/>
                    <field name = "nombre"/>
                    <field name = "apellidos"/>
                    <field name = "numero_colegiado"/>
                    <field name = "consulta"/>
                </group>
                <notebook>
                    <page string = "Pacientes atendidos">
                        <field name = "paciente_ids" readonly="1">
                            <list>
                                <field name = "nombre"/>
                                <field name = "apellidos"/>
                                <field name = "sintomas"/>
                            </list>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

**Vista de Lista**
- **ID**: `view_hospital_medico_list`
- **Columnas mostradas**:
  - ID Médico
  - Nombre
  - Apellidos
  - Número de colegiación
  - Consulta

**Código XML**:
```xml
<record id="view_hospital_medico_list" model="ir.ui.view">
    <field name="name">hospital.medico.list</field>
    <field name="model">modulo_hospital.medico</field>
    <field name="arch" type="xml">
        <list>
            <field name="id_medico"/>
            <field name="nombre"/>
            <field name="apellidos"/>
            <field name="numero_colegiado"/>
            <field name="consulta"/>
        </list>
    </field>
</record>
```

#### **Vistas de Diagnóstico**

**Vista de Formulario (Diagnósticos)**
- **Archivo**: `diagnostico_hospital_views.xml`
- **ID**: `view_hospital_diagnostico_form`
- **Estructura**:
  - Médico que realiza el diagnóstico (campo requerido, editable)
  - Paciente diagnosticado (campo requerido, editable)
  - Síntomas del paciente (solo lectura, relacionado del paciente)
  - Consulta del médico (solo lectura, relacionada del médico)

**Código XML**:
```xml
<record id="view_hospital_diagnostico_form" model="ir.ui.view">
    <field name="name">hospital.diagnostico.form</field>
    <field name="model">modulo_hospital.diagnostico</field>
    <field name="arch" type="xml">
        <form string = "Diagnósticos">
            <sheet>
                <group>
                    <field name = "medico_id"/>
                    <field name = "paciente_id"/>
                    <field name = "sintoma" readonly="1"/>
                    <field name = "consulta" readonly="1"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

**Vista de Lista**
- **ID**: `view_hospital_diagnostico_list`
- **Columnas mostradas**:
  - Médico
  - Paciente
  - Consulta

**Código XML**:
```xml
<record id="view_hospital_diagnostico_list" model="ir.ui.view">
    <field name="name">hospital.diagnostico.list</field>
    <field name="model">modulo_hospital.diagnostico</field>
    <field name="arch" type="xml">
        <list>
            <field name="medico_id"/>
            <field name="paciente_id"/>
            <field name="consulta"/>
        </list>
    </field>
</record>
```

### Descripción Técnica de las Vistas

**Componentes XML utilizados:**

- `<form>`: Define la vista de formulario con interfaz de edición/visualización
- `<list>`: Define la vista de lista para visualizar registros en tabla
- `<sheet>`: Contenedor principal para organizar el contenido del formulario
- `<group>`: Agrupa campos en filas y columnas
- `<notebook>`: Crea pestañas para organizar información relacionada
- `<page>`: Define el contenido de cada pestaña del notebook
- `<field>`: Muestra un campo del modelo
  - `readonly="1"`: Indica que el campo no puede ser editado
  - Atributos adicionales en `<list>` dentro de `<field>` para personalizar columnas

**Características principales:**

- Las vistas Many2many y One2many usan componentes anidados para mostrar relaciones
- Los campos relacionados mostrados en las listas son de solo lectura (readonly)
- La información se organiza de forma jerárquica usando pestañas (notebook/page)
- Las vistas de lista muestran un resumen de los campos más importantes

---

## Datos de Demostración (demo.xml)

El archivo `demo/demo.xml` contiene datos de ejemplo que se cargan automáticamente en modo demostración del módulo. Estos datos permiten probar la funcionalidad del módulo sin necesidad de crear registros manualmente.

**Código del archivo demo.xml**:
```xml
<odoo>
    <data>
        <record id="medico_hospital_racoonCity" model="modulo_hospital.medico">
            <field name="id_medico">MED-001</field>
            <field name="nombre">Leon</field>
            <field name="apellidos">S. Kennedy</field>
            <field name="numero_colegiado">RPD-1998</field>
            <field name="consulta">Mordedura por persona frenetica</field>
        </record>

        <record id="paciente_0" model="modulo_hospital.paciente">
            <field name="id_paciente">PAC-000</field>
            <field name="nombre">Diego</field>
            <field name="apellidos">Alonso Oro</field>
            <field name="sintomas">Fiebre, Cansancio, Ganas de comer cerebros</field>
        </record>

        <record id="diagnostico_virus_t" model="modulo_hospital.diagnostico">
            <field name="medico_id" ref="medico_hospital_racoonCity"/>
            <field name="paciente_id" ref="paciente_0"/>
        </record>

    </data>
</odoo>
```

**Descripción de los datos de demostración:**

1. **Médico**: Se crea un registro de médico con:
   - ID: `medico_hospital_racoonCity`
   - Nombre: Leon S. Kennedy
   - ID Médico: MED-001
   - Número de colegiación: RPD-1998
   - Consulta: Mordedura por persona frenetica

2. **Paciente**: Se crea un registro de paciente con:
   - ID: `paciente_0`
   - Nombre: Diego Alonso Oro
   - ID Paciente: PAC-000
   - Síntomas: Fiebre, Cansancio, Ganas de comer cerebros

3. **Diagnóstico**: Se crea un registro de diagnóstico que vincula:
   - ID: `diagnostico_virus_t`
   - Médico: referencia al registro `medico_hospital_racoonCity`
   - Paciente: referencia al registro `paciente_0`
   - Los campos `sintoma` y `consulta` se rellenan automáticamente desde los registros relacionados

**Atributos XML importantes:**

- `<record>`: Define un nuevo registro a crear
- `id`: Identificador único interno para referencias dentro del archivo XML
- `model`: Especifica el modelo de datos al que pertenece el registro
- `<field>`: Define el valor de un campo específico
- `ref`: Referencia a otro registro por su ID para crear relaciones

**Utilidad:**

Los datos de demostración son especialmente útiles para:
- Pruebas de funcionalidad del módulo
- Demostración de cómo se relacionan los modelos
- Validación de las vistas y formularios
- Verificar que las computaciones de campos (como `medico_ids` y `paciente_ids`) funcionen correctamente

---

## Docker y Configuración

### Servicios Incluidos

#### **Odoo 18** (Puerto 8069)
- Imagen: `odoo:18`
- Contenedor: `odoo_hospital`
- Volúmenes:
  - Datos de Odoo: `/var/lib/odoo`
  - Módulos personalizados: `./extra-addons:/mnt/extra-addons`
  - Configuración: `.config/:/etc/odoo/`

#### **PostgreSQL** (Base de Datos)
- Imagen: `postgres`
- Contenedor: `odoo_db_hospital`
- Usuario: `odoo`
- Contraseña: `odoo`
- Base de datos: `postgres`
- Volumen: `db_data:/var/lib/postgresql`

#### **pgAdmin 4** (Gestor de Base de Datos)
- Imagen: `dpage/pgadmin4:latest`
- Puerto: 5050
- Email: `admin@admin.com`
- Contraseña: `admin1234`
- Volumen: `pgadmin_data:/var/lib/pgadmin`

### Archivo `docker-compose.yml`

```yaml
name: odoo_modulo_hospital

services:
  odoo:
    image: odoo:18
    container_name: odoo_hospital
    ports:
      - "8069:8069"
    depends_on:
      - db
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo_data:/var/lib/odoo
      - ./extra-addons:/mnt/extra-addons
      - .config/:/etc/odoo/

  db:
    image: postgres
    container_name: odoo_db_hospital
    environment:
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_DB=postgres
    volumes:
      - db_data:/var/lib/postgresql

  pgadmin:
    image: dpage/pgadmin4:latest
    restart: always
    depends_on:
      - db
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin1234
    volumes:
      - pgadmin_data:/var/lib/pgadmin

volumes:
  odoo_data:
  addons_path:
  db_data:
  pgadmin_data:
```

---

## Instalación y Uso

### Requisitos Previos
- Docker instalado
- Docker Compose instalado
- Terminal/CMD disponible

### Pasos de Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   cd Tarea_18_ModuloRelaciones_Hospital
   ```

2. **Iniciar los servicios con Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Acceder a Odoo:**
   - URL: `http://localhost:8069`
   - Usuario: `admin`
   - Contraseña: (configurada en Odoo)

4. **Acceder a pgAdmin (opcional):**
   - URL: `http://localhost:5050`
   - Email: `admin@admin.com`
   - Contraseña: `admin1234`

### Instalar el Módulo en Odoo

1. Ir a **Aplicaciones** en el menú principal
2. Actualizar la lista de aplicaciones
3. Buscar "modulo_hospital"
4. Hacer clic en **Instalar**

---

## Configuración de Odoo (`config/odoo.conf`)

```ini
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = $pbkdf2-sha512$...
```

### Parámetros Principales
- `addons_path`: Ruta donde Odoo busca los módulos personalizados
- `data_dir`: Directorio de datos de Odoo
- `admin_passwd`: Contraseña del administrador (hasheada)

---

## Control de Acceso

El módulo incluye archivo `ir.model.access.csv` para controlar los permisos de lectura, escritura, creación y eliminación de registros según el rol del usuario.

---

## Tecnologías Utilizadas

- **Odoo 18**: Framework web para gestión empresarial
- **Python 3.x**: Lenguaje de programación backend
- **PostgreSQL**: Sistema de gestión de base de datos
- **Docker**: Contenedorización de servicios
- **XML**: Definición de vistas y menús
- **CSV**: Control de acceso

---

## Autores

- **Módulo Hospital**: CabbaGG Corp.

---

## Notas

- El módulo está diseñado para Odoo 18
- Incluye datos de demostración para pruebas
- El control de acceso debe configurarse según los roles de usuario
- La base de datos se persiste en volúmenes de Docker

---

## Soporte

Para obtener ayuda con Odoo, consulta la [documentación oficial de Odoo](https://www.odoo.com/documentation).

---

**Última actualización**: Enero 2026  
**Versión del Proyecto**: 0.1

