# Potable water calculations based
# AUTHOR: PIOTR JAŻDŻYK / 2020.07.24
# REFERENCES:
# [1] EN 806-3 : 2006
# [2] Equations based on "Calculation methods, for design of flow rates and peak flow-rates in print
# for water installations inside buildings" (ISSSN 2344-2409)
# [3] Kazimierz Żarski - Projektowanie Kotłowni Wodnych (2014)

# ---------------------------------FIXTURE OBJECT AS A PLACEHOLDER FOR LU----------------------
class Fixture:
    # DEFAULT FIELDS
    __LU = 0
    __name = '';

    # CONSTRUCTOR
    def __init__(self, inLu, inName):
        self.__LU = inLu
        self.__name = inName

    # CALCULATE TOTAL LUS BASED ON PROVIDED FIXTURE QUANTITY
    def calcTotLU(self, qty=0):
        if (qty < 0):
            raise ValueError('qty < 0, check your input')
        else:
            return self.__LU * qty

    # CALCULATE TOTAL FLOW BASED ON PROVIDED FIXTURE QUANTITY
    def calcTotLSFlow(self, qty=0):
        if (qty < 0):
            raise ValueError('qty < 0, check your input')
        else:
            return self.calcTotLU(qty) * 0.1;  # l/s

    def getName(self):
        return self.__name;

    def getBaseLU(self):
        return self.__LU

    # ---------------------------------FIXTURE DATABASE CLASS----------------------


class FixtureDataBase:

    def __init__(self):
        # DICTIONARY DATA TYPE: KEY - VALUE --> LU / NAME
        self.__fixtList = {

            'WashBasin': Fixture(1, 'Wash basin (Umywalka)'),
            'Bidet': Fixture(1, 'Bidet'),
            'KitchenSink': Fixture(2, 'Kitchen sink (Zlew kuchenny)'),
            'WashingMachine': Fixture(2, 'Washing machine (Pralka)'),
            'DishWasher': Fixture(2, 'Dish washer machine (Zmywarka)'),
            'Urinal': Fixture(3, 'Urinal (Pisuar)'),
            'BathDomestic': Fixture(4, 'Bath domestic (wylewka prysznicowa)'),
            'GardenTap': Fixture(5, 'Grden or garage tap (kurek ogrodowy)'),
            'NonDomesticSink': Fixture(8, 'Non domestic sink (zlew przemysłowt)'),
            'FlushValve20': Fixture(15, 'Flush valve DN15 (Zawor pluczacy Dn15)')

        }

    def getList(self):
        return self.__fixtList


# ---------------------------------POTABLE WATER CALC CLASS----------------------
class PotableWater:

    # TOOL METHODS

    # CONVERTS LUs to flow in SI units [m3/s]
    @staticmethod
    def convToSI(sumLU=0):  # LU
        volFlow = sumLU * 0.1  # l/s
        return volFlow / 1000  # m3/s

    # CONVRETS flow in SI units to LUs
    @staticmethod
    def convToLU(volFlow=0):  # m3/s
        tempFlow = volFlow * 1000  # l/s
        return tempFlow / 0.1  # LU

    # Converts LUs to l/s
    @staticmethod
    def convLuToLs(sumLU=0):
        return sumLU * 0.1;

    # Convers l/s to LUs
    @staticmethod
    def convLsToLU(volFlowLs=0):
        return volFlowLs / 0.1;

    @staticmethod
    def calcDCoef(sumLU=0):
        if (sumLU < 0):
            raise ValueError("Flow < 0, check your input")
        if (sumLU <= 300):
            return 0.256
        else:
            return 0.0482

    @staticmethod
    def calcECoef(sumLU=0):
        if (sumLU < 0):
            raise ValueError("Flow < 0, check your input")
        if (sumLU <= 300):
            return 0.321
        else:
            return 0.614

        # MAIN CALCULATION METHODS

    # CALCULATE DESIGN FLOWRATE (K.ZARSKI POWER APPROXIMATE)
    @staticmethod
    def calcDesignFlow(normFlows=0.0, constFlows=0.0):  # Flow inputs in l/s
        if (normFlows <= 0):
            return 0.0 + constFlows
        else:
            LU = PotableWater.convLsToLU(normFlows)
            d = PotableWater.calcDCoef(LU)
            e = PotableWater.calcECoef(LU)
            return d * (LU ** e) + constFlows

    # CALCULATE TOTAL DESIGN FLOWRATE
    @staticmethod
    def calcTotalDesignFlow(normFlows=[], constFlows=[]):
        if (len(normFlows) <= 0):
            return 0 + constFlows
        else:
            totalNormFlow = 0;
            totalConstFlow = 0;
            for nFlow in normFlows:
                totalNormFlow += nFlow
            for cFlow in constFlows:
                totalConstFlow += cFlow
            return PotableWater.calcDesignFlow(totalNormFlow) + totalConstFlow


# ----------------------------------------------------------------------
# TESTY JEDNOSTKOWE
print('TEST WERSJI JEDNOSTKOWEJ')
Lus = 400
volFlow = PotableWater.convLuToLs(Lus)
finalFlow = PotableWater.calcDesignFlow(volFlow, 0)
print(finalFlow)

print('TEST WERSJI Z ARRAYAMI')
totalNormFlows = {1, 2, 3, 4, 10}
totalConstFlows = {0, 0}

totalFlow = PotableWater.calcTotalDesignFlow(totalNormFlows, totalConstFlows)
print(totalFlow)

print('TEST KLASY FIXTURE')
przyklad = Fixture(2, 'zajac')
aaa = przyklad.getBaseLU()
bbb = przyklad.calcTotLU(10)
print('  BASE LU = ' + str(aaa))
print('  FOR 10 units = ' + str(bbb))

print('TEST BAZY DANYCH')
baza = FixtureDataBase()
listaPrzyborow = baza.getList()
nazwa = listaPrzyborow.get('WashBasin').getName()
baseLU = listaPrzyborow.get('WashBasin').getBaseLU()
print('PRZYBOR: ' + nazwa + ' LU= ' + str(baseLU))

