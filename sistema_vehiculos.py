
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
import logging
import tkinter as tk
from tkinter import ttk, messagebox


# ==================================================
# 1. CONFIGURACION DEL SISTEMA DE LOGS
# ==================================================

logging.basicConfig(
    filename="vehiculos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger("SistemaVehiculos")


# ==================================================
# 2. EXCEPCION PERSONALIZADA
# ==================================================

class ErrorValidacion(Exception):
    """Controla los errores de validacion del sistema."""
    pass


# ==================================================
# 3. CLASE ABSTRACTA VEHICULO
# ==================================================

class Vehiculo(ABC):

    def __init__(self, marca, modelo, precio):

        if not isinstance(marca, str) or not marca.strip():
            raise ErrorValidacion("La marca es obligatoria.")

        if not isinstance(modelo, str) or not modelo.strip():
            raise ErrorValidacion("El modelo es obligatorio.")

        self._marca = marca.strip()
        self._modelo = modelo.strip()
        self._precio = self.convertir_decimal(precio)

        if self._precio <= 0:
            raise ErrorValidacion(
                "El precio debe ser mayor que cero."
            )

        self._velocidad_actual = 0

    # ----------------------------------------------
    # METODO AUXILIAR PARA VALIDAR NUMEROS
    # ----------------------------------------------

    @staticmethod
    def convertir_decimal(valor):

        if isinstance(valor, bool):
            raise ErrorValidacion("El valor debe ser numerico.")

        try:
            numero = Decimal(str(valor))

            if not numero.is_finite():
                raise ErrorValidacion(
                    "El valor debe ser un numero finito."
                )

            return numero

        except (InvalidOperation, ValueError, TypeError) as error:
            raise ErrorValidacion(
                "Ingrese un valor numerico valido."
            ) from error

    # ----------------------------------------------
    # PROPIEDADES Y ENCAPSULAMIENTO
    # ----------------------------------------------

    @property
    def marca(self):
        return self._marca

    @property
    def modelo(self):
        return self._modelo

    @property
    def precio(self):
        return self._precio

    @property
    def velocidad_actual(self):
        return self._velocidad_actual

    # ----------------------------------------------
    # METODO PARA ACELERAR
    # ----------------------------------------------

    def acelerar(self, incremento=10, modo_deportivo=False):

        incremento = self.convertir_decimal(incremento)

        if incremento <= 0:
            raise ErrorValidacion(
                "El incremento debe ser mayor que cero."
            )

        if not isinstance(modo_deportivo, bool):
            raise ErrorValidacion(
                "El modo deportivo debe ser verdadero o falso."
            )

        if modo_deportivo:
            incremento *= Decimal("2")

        self._velocidad_actual += incremento

        logger.info(
            "%s %s acelero. Velocidad actual: %s km/h",
            self.marca,
            self.modelo,
            self.velocidad_actual
        )

        return self._velocidad_actual

    # ----------------------------------------------
    # METODO PARA DETENER
    # ----------------------------------------------

    def detener(self):

        self._velocidad_actual = Decimal("0")

        logger.info(
            "%s %s se detuvo.",
            self.marca,
            self.modelo
        )

        return self._velocidad_actual

    # ----------------------------------------------
    # CALCULO GENERAL DE COSTOS
    # ----------------------------------------------

    def calcular_total(self, impuesto=0, descuento=0,
                       seguro=0):

        impuesto = self.convertir_decimal(impuesto)
        descuento = self.convertir_decimal(descuento)
        seguro = self.convertir_decimal(seguro)

        if not Decimal("0") <= impuesto <= Decimal("100"):
            raise ErrorValidacion(
                "El impuesto debe estar entre 0 y 100 %."
            )

        if descuento < 0 or descuento > self.precio:
            raise ErrorValidacion(
                "El descuento no puede superar el precio."
            )

        if seguro < 0:
            raise ErrorValidacion(
                "El seguro no puede ser negativo."
            )

        subtotal = self.precio - descuento

        valor_impuesto = (
            subtotal * impuesto / Decimal("100")
        )

        total = subtotal + valor_impuesto + seguro

        total = total.quantize(Decimal("0.01"))

        logger.info(
            "Costo calculado para %s %s. "
            "Precio: %s, Impuesto: %s%%, "
            "Descuento: %s, Seguro: %s, Total: %s",
            self.marca,
            self.modelo,
            self.precio,
            impuesto,
            descuento,
            seguro,
            total
        )

        return total

    # ----------------------------------------------
    # METODOS ABSTRACTOS
    # ----------------------------------------------

    @abstractmethod
    def calcular_costo(self, impuesto=0, descuento=0,
                       seguro=0):
        pass

    @abstractmethod
    def describir(self):
        pass


# ==================================================
# 4. VEHICULO DE COMBUSTION
# ==================================================

class VehiculoCombustion(Vehiculo):

    def __init__(self, marca, modelo, precio, cilindraje):

        super().__init__(marca, modelo, precio)

        self._cilindraje = self.convertir_decimal(cilindraje)

        if self._cilindraje <= 0:
            raise ErrorValidacion(
                "El cilindraje debe ser mayor que cero."
            )

        logger.info(
            "Vehiculo de combustion creado: %s %s",
            marca,
            modelo
        )

    @property
    def cilindraje(self):
        return self._cilindraje

    def calcular_costo(self, impuesto=0, descuento=0,
                       seguro=0):

        return self.calcular_total(
            impuesto, descuento, seguro
        )

    def describir(self):

        return (
            "TIPO: VEHICULO DE COMBUSTION\n"
            f"Marca: {self.marca}\n"
            f"Modelo: {self.modelo}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Cilindraje: {self.cilindraje} cc\n"
            f"Velocidad: {self.velocidad_actual} km/h"
        )


# ==================================================
# 5. VEHICULO ELECTRICO
# ==================================================

class VehiculoElectrico(Vehiculo):

    def __init__(self, marca, modelo, precio, autonomia):

        super().__init__(marca, modelo, precio)

        self._autonomia = self.convertir_decimal(autonomia)

        if self._autonomia <= 0:
            raise ErrorValidacion(
                "La autonomia debe ser mayor que cero."
            )

        logger.info(
            "Vehiculo electrico creado: %s %s",
            marca,
            modelo
        )

    @property
    def autonomia(self):
        return self._autonomia

    def calcular_costo(self, impuesto=0, descuento=0,
                       seguro=0):

        return self.calcular_total(
            impuesto, descuento, seguro
        )

    def describir(self):

        return (
            "TIPO: VEHICULO ELECTRICO\n"
            f"Marca: {self.marca}\n"
            f"Modelo: {self.modelo}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Autonomia: {self.autonomia} km\n"
            f"Velocidad: {self.velocidad_actual} km/h"
        )


# ==================================================
# 6. VEHICULO HIBRIDO
# ==================================================

class VehiculoHibrido(Vehiculo):

    def __init__(self, marca, modelo, precio,
                 autonomia_electrica):

        super().__init__(marca, modelo, precio)

        self._autonomia_electrica = (
            self.convertir_decimal(autonomia_electrica)
        )

        if self._autonomia_electrica <= 0:
            raise ErrorValidacion(
                "La autonomia electrica debe ser mayor que cero."
            )

        logger.info(
            "Vehiculo hibrido creado: %s %s",
            marca,
            modelo
        )

    @property
    def autonomia_electrica(self):
        return self._autonomia_electrica

    def calcular_costo(self, impuesto=0, descuento=0,
                       seguro=0):

        return self.calcular_total(
            impuesto, descuento, seguro
        )

    def describir(self):

        return (
            "TIPO: VEHICULO HIBRIDO\n"
            f"Marca: {self.marca}\n"
            f"Modelo: {self.modelo}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Autonomia electrica: "
            f"{self.autonomia_electrica} km\n"
            f"Velocidad: {self.velocidad_actual} km/h"
        )


# ==================================================
# 7. INTERFAZ GRAFICA CON TKINTER
# ==================================================

class SistemaVehiculos:

    def __init__(self, ventana):

        self.ventana = ventana
        self.vehiculo = None

        self.ventana.title(
            "Sistema de Vehiculos Inteligentes"
        )

        self.ventana.geometry("650x720")
        self.ventana.resizable(False, False)

        logger.info("Sistema iniciado correctamente.")

        self.crear_interfaz()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

    # ----------------------------------------------
    # CREACION DE LA INTERFAZ
    # ----------------------------------------------

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="SISTEMA DE VEHICULOS INTELIGENTES",
            font=("Arial", 17, "bold")
        )

        titulo.pack(pady=15)

        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=5)

        # Tipo de vehiculo
        tk.Label(
            formulario,
            text="Tipo de vehiculo:"
        ).grid(row=0, column=0, sticky="w", pady=6)

        self.tipo = ttk.Combobox(
            formulario,
            values=[
                "Combustion",
                "Electrico",
                "Hibrido"
            ],
            state="readonly",
            width=30
        )

        self.tipo.grid(row=0, column=1, pady=6)
        self.tipo.current(0)

        # Marca
        tk.Label(
            formulario,
            text="Marca:"
        ).grid(row=1, column=0, sticky="w", pady=6)

        self.marca = tk.Entry(formulario, width=33)
        self.marca.grid(row=1, column=1, pady=6)

        # Modelo
        tk.Label(
            formulario,
            text="Modelo:"
        ).grid(row=2, column=0, sticky="w", pady=6)

        self.modelo = tk.Entry(formulario, width=33)
        self.modelo.grid(row=2, column=1, pady=6)

        # Precio
        tk.Label(
            formulario,
            text="Precio:"
        ).grid(row=3, column=0, sticky="w", pady=6)

        self.precio = tk.Entry(formulario, width=33)
        self.precio.grid(row=3, column=1, pady=6)

        # Dato tecnico
        tk.Label(
            formulario,
            text="Cilindraje / Autonomia:"
        ).grid(row=4, column=0, sticky="w", pady=6)

        self.dato_tecnico = tk.Entry(
            formulario,
            width=33
        )

        self.dato_tecnico.grid(row=4, column=1, pady=6)

        # Impuesto
        tk.Label(
            formulario,
            text="Impuesto (%):"
        ).grid(row=5, column=0, sticky="w", pady=6)

        self.impuesto = tk.Entry(formulario, width=33)
        self.impuesto.insert(0, "0")
        self.impuesto.grid(row=5, column=1, pady=6)

        # Descuento
        tk.Label(
            formulario,
            text="Descuento ($):"
        ).grid(row=6, column=0, sticky="w", pady=6)

        self.descuento = tk.Entry(formulario, width=33)
        self.descuento.insert(0, "0")
        self.descuento.grid(row=6, column=1, pady=6)

        # Seguro
        tk.Label(
            formulario,
            text="Seguro ($):"
        ).grid(row=7, column=0, sticky="w", pady=6)

        self.seguro = tk.Entry(formulario, width=33)
        self.seguro.insert(0, "0")
        self.seguro.grid(row=7, column=1, pady=6)

        # Botones
        botones = tk.Frame(self.ventana)
        botones.pack(pady=15)

        tk.Button(
            botones,
            text="Registrar vehiculo",
            width=20,
            command=self.registrar_vehiculo
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            botones,
            text="Calcular costo",
            width=20,
            command=self.calcular_costo
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            botones,
            text="Acelerar",
            width=20,
            command=self.acelerar_vehiculo
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            botones,
            text="Detener",
            width=20,
            command=self.detener_vehiculo
        ).grid(row=1, column=1, padx=5, pady=5)

        # Resultado
        tk.Label(
            self.ventana,
            text="INFORMACION DEL VEHICULO",
            font=("Arial", 12, "bold")
        ).pack(pady=8)

        self.resultado = tk.Text(
            self.ventana,
            width=65,
            height=11,
            font=("Consolas", 10),
            state="disabled"
        )

        self.resultado.pack(pady=5)

    # ----------------------------------------------
    # MOSTRAR INFORMACION
    # ----------------------------------------------

    def mostrar_resultado(self, texto):

        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, texto)
        self.resultado.config(state="disabled")

    # ----------------------------------------------
    # REGISTRAR VEHICULO
    # ----------------------------------------------

    def registrar_vehiculo(self):

        try:

            tipo = self.tipo.get()
            marca = self.marca.get().strip()
            modelo = self.modelo.get().strip()
            precio = self.precio.get().strip()
            dato = self.dato_tecnico.get().strip()

            if not dato:
                raise ErrorValidacion(
                    "Debe ingresar el dato tecnico."
                )

            if tipo == "Combustion":

                self.vehiculo = VehiculoCombustion(
                    marca, modelo, precio, dato
                )

            elif tipo == "Electrico":

                self.vehiculo = VehiculoElectrico(
                    marca, modelo, precio, dato
                )

            elif tipo == "Hibrido":

                self.vehiculo = VehiculoHibrido(
                    marca, modelo, precio, dato
                )

            else:

                raise ErrorValidacion(
                    "Seleccione un tipo de vehiculo."
                )

            logger.info(
                "Registro exitoso: %s %s",
                marca,
                modelo
            )

            self.mostrar_resultado(
                self.vehiculo.describir()
            )

            messagebox.showinfo(
                "Registro exitoso",
                "Vehiculo registrado correctamente."
            )

        except ErrorValidacion as error:

            logger.warning(
                "Error de validacion al registrar: %s",
                error
            )

            messagebox.showerror(
                "Error de validacion",
                str(error)
            )

        except Exception:

            logger.exception(
                "Error inesperado durante el registro."
            )

            messagebox.showerror(
                "Error",
                "Ocurrio un error inesperado."
            )

    # ----------------------------------------------
    # CALCULAR COSTO
    # ----------------------------------------------

    def calcular_costo(self):

        try:

            if self.vehiculo is None:
                raise ErrorValidacion(
                    "Primero debe registrar un vehiculo."
                )

            impuesto = self.impuesto.get().strip() or "0"
            descuento = self.descuento.get().strip() or "0"
            seguro = self.seguro.get().strip() or "0"

            total = self.vehiculo.calcular_costo(
                impuesto=impuesto,
                descuento=descuento,
                seguro=seguro
            )

            texto = (
                self.vehiculo.describir()
                + "\n\n"
                + f"Impuesto: {impuesto}%\n"
                + f"Descuento: ${Decimal(descuento):,.2f}\n"
                + f"Seguro: ${Decimal(seguro):,.2f}\n"
                + f"COSTO FINAL: ${total:,.2f}"
            )

            self.mostrar_resultado(texto)

            messagebox.showinfo(
                "Calculo realizado",
                f"El costo final es: ${total:,.2f}"
            )

        except ErrorValidacion as error:

            logger.warning(
                "Error en el calculo de costos: %s",
                error
            )

            messagebox.showerror(
                "Error de calculo",
                str(error)
            )

        except Exception:

            logger.exception(
                "Error inesperado durante el calculo."
            )

            messagebox.showerror(
                "Error",
                "No fue posible completar el calculo."
            )

    # ----------------------------------------------
    # ACELERAR VEHICULO
    # ----------------------------------------------

    def acelerar_vehiculo(self):

        try:

            if self.vehiculo is None:
                raise ErrorValidacion(
                    "Primero debe registrar un vehiculo."
                )

            velocidad = self.vehiculo.acelerar()

            self.mostrar_resultado(
                self.vehiculo.describir()
                + f"\n\nNueva velocidad: {velocidad} km/h"
            )

        except ErrorValidacion as error:

            logger.warning(
                "Error al acelerar: %s",
                error
            )

            messagebox.showerror(
                "Error",
                str(error)
            )

        except Exception:

            logger.exception(
                "Error inesperado al acelerar."
            )

            messagebox.showerror(
                "Error",
                "No fue posible acelerar el vehiculo."
            )

    # ----------------------------------------------
    # DETENER VEHICULO
    # ----------------------------------------------

    def detener_vehiculo(self):

        try:

            if self.vehiculo is None:
                raise ErrorValidacion(
                    "Primero debe registrar un vehiculo."
                )

            velocidad = self.vehiculo.detener()

            self.mostrar_resultado(
                self.vehiculo.describir()
                + f"\n\nVelocidad actual: {velocidad} km/h"
            )

        except ErrorValidacion as error:

            logger.warning(
                "Error al detener: %s",
                error
            )

            messagebox.showerror(
                "Error",
                str(error)
            )

        except Exception:

            logger.exception(
                "Error inesperado al detener."
            )

            messagebox.showerror(
                "Error",
                "No fue posible detener el vehiculo."
            )

    # ----------------------------------------------
    # CERRAR APLICACION
    # ----------------------------------------------

    def cerrar_aplicacion(self):

        logger.info(
            "Sistema de Vehiculos Inteligentes cerrado."
        )

        self.ventana.destroy()


# ==================================================
# 8. EJECUCION PRINCIPAL
# ==================================================

if __name__ == "__main__":

    try:

        ventana = tk.Tk()

        aplicacion = SistemaVehiculos(ventana)

        ventana.mainloop()

    except Exception:

        logger.exception(
            "Error critico durante la ejecucion."
        )

        raise
