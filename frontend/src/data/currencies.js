import { createResource } from "frappe-ui"

const agencyCurrency = createResource({
	url: "hrms.api.get_agency_currencies",
	auto: true,
})

const currencySymbols = createResource({
	url: "hrms.api.get_currency_symbols",
	auto: true,
})

export function getCompanyCurrency(agency) {
	return agencyCurrency?.data?.[agency]?.[0]
}

export function getCompanyCurrencySymbol(agency) {
	return agencyCurrency?.data?.[agency]?.[1]
}

export function getCurrencySymbol(currency) {
	return currencySymbols?.data?.[currency]
}
