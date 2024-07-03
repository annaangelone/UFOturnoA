from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getShapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct shape as s
                from sighting s
                where year(s.datetime) = %s
                order by s
                """
        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row["s"])
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select *
                    from state
                    """
        cursor.execute(query,)

        for row in cursor:
            result.append(Stato(**row))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(s1, s2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select n.state1 as state1, n.state2 as state2
                from neighbor n
                where n.state1 = %s and n.state2 = %s and n.state1 < n.state2
                """
        cursor.execute(query, (s1, s2))

        for row in cursor:
            result.append((row["state1"], row["state2"]))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(s1, s2, shape, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT COUNT(*) as peso
                    FROM sighting s1
                    WHERE (s1.state = %s OR s1.state = %s) AND YEAR(s1.datetime) = %s 
                    AND s1.shape = %s
                    """
        cursor.execute(query, (s1, s2, year, shape))

        for row in cursor:
            result.append(row["peso"])
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result
