#!/usr/bin/python
#
# ml 2016
#
# convert mbs csv to homebank csv
#
# python mbs2homebank.py CSV
#
### mbs csv header
# 0 Auftragskonto
# 1 Buchungstag
# 2 Valutadatum
# 3 Buchungstext
# 4 Verwendungszweck
# 5 Beguenstigter/Zahlungspflichtiger
# 6 Kontonummer
# 7 BLZ
# 8 Betrag
# 9 Waehrung
# 10 Info
#
#
### homebank header
# date		format must be DD-MM-YY
# paymode	from 0=none to 10=FI fee
# info		a string
# payee		a payee name
# memo		a string
# amount	a number with a '.' or ',' as decimal separator, ex: -24.12 or 36,75
# category	a full category name (category, or category:subcategory)
# tags		tags separated by space, tag is mandatory since v4.5
#
#
### classification
# date		= Valutadatum
# paymode	= Buchungstext (as int)
# info		= Buchungstext (as string)
# payee		= Beguenstigter/Zahlungspflichtiger
# memo		= Verwendungszweck
# amount	= Betrag
# category	= empty
# tags		= empty
#
### paymode
# 0 = none			ABSCHLUSS
# 1 = kreditkarte		na
# 2 = schecks			na
# 3 = bargeld 			GELDAUTOMAT
# 4 = ueberweisung		ONLINE-UEBERWEISUNG
# 5 = zwischen konten		"SEPA UEBERTRAG SOLL"
# 6 = einzugsermaechtigung	na
# 7 = dauerauftrag		DAUERAUFTRAG
# 8 = kartenzahlung		KARTENZAHLUNG, "SONSTIGER EINZUG"
# 9 = einzahlung		GUTSCHRIFT,EINZAHLUNG,LOHN  GEHALT, "SEPA UEBERTRAG HABEN"
# 10= FI Abgabe			na
# 11= lastschrift		FOLGELASTSCHRIFT/LASTSCHRIFT/SEPA-ELV-LASTSCHRIFT/ERSTLASTSCHRIFT

paymode = {
	"ABSCHLUSS": 0,
	"GELDAUTOMAT": 3,
	"ONLINE-UEBERWEISUNG": 4,
	"SEPA UEBERTRAG SOLL": 4,
	"DAUERAUFTRAG": 7,
	"KARTENZAHLUNG": 8,
	"SONSTIGER EINZUG": 8,
	"GUTSCHRIFT": 9,
	"EINZAHLUNG": 9,
	"LOHN  GEHALT": 9,
	"SEPA UEBERTRAG HABEN": 9,
	"FOLGELASTSCHRIFT":11,
	"LASTSCHRIFT":11,
	"SEPA-ELV-LASTSCHRIFT":11,
	"ERSTLASTSCHRIFT":11,
}


### imports
import csv
import argparse
import os
import sys
import datetime

### parse
parser = argparse.ArgumentParser()
parser.add_argument("csv", help="csv from mbs")
args = parser.parse_args()
incsv = args.csv


### functions
def remove_quotes(string):
	if string.startswith('"') and string.endswith('"'):
		string = string[1:-1]
	return string

def convert_date(date):
	return datetime.datetime.strptime(date, '%d.%m.%y').strftime('%d/%m/%Y')


### read csv
try:
	with open(incsv, 'rb') as csvfile:
		reader = csv.reader(csvfile,delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			if remove_quotes(row[0]) == "Auftragskonto":
				continue

			#date;paymode;info;payee;memo;balance;--cat;--tag
			print "%s;%s;%s;%s;%s;%s;;" % (
				convert_date(remove_quotes(row[2])),
				paymode[remove_quotes(row[3])],
				remove_quotes(row[3]),
				remove_quotes(row[5]),
				remove_quotes(row[4]),
				remove_quotes(row[8]),
			)


except IOError:
	print incsv + " not found"

except:
	print "Unexpected error:", sys.exc_info()[0]
else:
	csvfile.close()
