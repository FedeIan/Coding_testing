from enum import Enum


class PlaceOrderErrorCode(str, Enum):
    CANTLEGALYTRADEEXCEPTION = "CantLegalyTradeException"
    INSTRUMENTNOTFOUND = "InstrumentNotFound"
    INSUFFICIENTFREEFORSTOCKSEXCEPTION = "InsufficientFreeForStocksException"
    INSUFFICIENTRESOURCES = "InsufficientResources"
    INSUFFICIENTVALUEFORSTOCKSSELL = "InsufficientValueForStocksSell"
    INVALIDVALUE = "InvalidValue"
    LIMITPRICEMISSING = "LimitPriceMissing"
    MAXEQUITYBUYQUANTITYEXCEEDED = "MaxEquityBuyQuantityExceeded"
    MAXEQUITYSELLQUANTITYEXCEEDED = "MaxEquitySellQuantityExceeded"
    MAXQUANTITYEXCEEDED = "MaxQuantityExceeded"
    MINQUANTITYEXCEEDED = "MinQuantityExceeded"
    MINVALUEEXCEEDED = "MinValueExceeded"
    NOTAVAILABLEFORREALMONEYACCOUNTS = "NotAvailableForRealMoneyAccounts"
    NOTELIGIBLEFORISA = "NotEligibleForISA"
    PRICETOOFAR = "PriceTooFar"
    QUANTITYMISSING = "QuantityMissing"
    SELLINGEQUITYNOTOWNED = "SellingEquityNotOwned"
    SHARELENDINGAGREEMENTNOTACCEPTED = "ShareLendingAgreementNotAccepted"
    STOPPRICEMISSING = "StopPriceMissing"
    TARGETPRICETOOCLOSE = "TargetPriceTooClose"
    TARGETPRICETOOFAR = "TargetPriceTooFar"
    TICKERMISSING = "TickerMissing"
    UNDEFINED = "UNDEFINED"

    def __str__(self) -> str:
        return str(self.value)
