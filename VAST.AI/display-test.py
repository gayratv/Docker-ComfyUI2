from PY_mysql.vast_offers_display import DisplayOffers



if __name__ == "__main__":
    with DisplayOffers(60) as display:
        display.display_results()
