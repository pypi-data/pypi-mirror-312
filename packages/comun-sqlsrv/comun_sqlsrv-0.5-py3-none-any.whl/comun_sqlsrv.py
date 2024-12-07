import pymssql


class Sql:
    def __init__(self, servidor, database, user, passw, autocommit=True, as_dict=True):
        self.conexion = pymssql.connect(server=servidor, user=user, password=passw, database=database, autocommit=autocommit)
        self.cursor = self.conexion.cursor(as_dict=as_dict)

    def cerrar_conexion(self):
        self.conexion.close()

    def ejecutar(self, texto, *parametros):
        """Ejecutar sentencia en la bd

        conn.ejecutar("UPDATE [dbo].[T_ENTR_MERC_CABECERA] SET ALBARAN=%s, ENTREGA_MM = %s, ENTREGA_EWM=%s, ID_ESTADO_SAP=1 WHERE DESCARGA=%s",
        delivery_note, mm_delivery, ewm_delivery, unload_number)
        """
        try:
            if len(parametros):
                if type(parametros[0]) == tuple:
                    parametros = parametros[0]
            self.cursor.execute(texto, parametros)
            self.conexion.commit()
        except Exception as e:
            print(texto)
            print(parametros)
            print(e)
            raise Exception(e)

    def ejecutar_varios(self, texto, data: list):
        """Inserciones masivas en la bd

        data = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        conn.ejecutar_varios("INSERT INTO [dbo].[T_TRINIDAD_XLS_VENTA_MENSUAL] VALUES (%s, %s, %s)", data)

        """
        try:
            self.cursor.executemany(texto, data)
            self.conexion.commit()
        except Exception as e:
            print(texto)
            print(e)
            raise Exception(e)

    def consultar(self, consulta, params=None):
        """Consulta en la bd

        conn.consultar("SELECT * FROM [DW_Procesos].[dbo].[T_ENTR_MERC_CABECERA] WHERE DESCARGA=%s", unload_number)
        """
        self.cursor.execute(consulta, params)
        return self.cursor.fetchall()

