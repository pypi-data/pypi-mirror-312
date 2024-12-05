from hotel_coupon_app_package_alexandermamani.report_pdf import ReportPDF


import datetime
if __name__ == '__main__':

    coupon_gral_information = {}
    coupon_gral_information['1'] = {}
    coupon_gral_information['1']['title'] = "December offer"
    coupon_gral_information['1']['how_many_have_redeemed'] = "2"
    coupon_gral_information['1']['how_many_have_used'] = "1"
    coupon_gral_information['1']['quantity'] = "30"
    coupon_gral_information['1']['discount'] = "10"
    coupon_gral_information['2'] = {}
    coupon_gral_information['2']['title'] = "January offer"
    coupon_gral_information['2']['how_many_have_redeemed'] = "0"
    coupon_gral_information['2']['how_many_have_used'] = "0"
    coupon_gral_information['2']['quantity'] = "15"
    coupon_gral_information['2']['discount'] = "5"

    user_interactions = {}
    user_interactions["1"] = {}
    user_interactions["1"]['view'] = 0
    user_interactions["1"]['redeem'] = 0
    user_interactions["1"]['coupon_title'] = "Winter promotion"
    user_interactions["2"] = {}
    user_interactions["2"]['view'] = 10
    user_interactions["2"]['redeem'] = 10
    user_interactions["2"]['coupon_title'] = "Summer promotion"

    report = ReportPDF(user_interactions, coupon_gral_information,datetime.datetime.now().date(),"Dublin hotel","report.pdf")
    print(report.generate())