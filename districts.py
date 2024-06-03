import re, os

gu1_M = r"^1$"
gu2_M = r"(801|802|803|805|807|812|813|815)"
gu3_M = r"(501|502|504|505|506|507|508|509|510|511|512|513)"
gu4_M = r"(701|702|703|705|707|708|709|710|711|712|713|714|715|716|717)"
gu5_M = r"(201|202|203|205|206|207|208|209|210|211|212|213|214|215|216)"
gu6_M = r"(301|302|303|304|305|306|307|308|309|310|311|312|314|315|316|317|318)"
gu7_M = r"(401|402|403|404|405|407|408|409|411|412|413|414|415)"
gu8_M = r"(601|602|603|604|605|606|607|608|609|610|611|612|613|614|616|617)"
gu9_M = r"(901|902|903|904|905|906|907)"
gu10_M = r"(101|102|103|104|105|106|107|108|109|110)"

gu1_MO = r"(^5$|16$|20|45|116$)"
gu2_MO = r"(28|30|^32$|^42$|132)"
gu3_MO = r"(^4$|^9$|11$|^27$|33|35|^52$|59|152|227|327|427|527)"
gu4_MO = r"(^7$|36|37|39|43|46|51|^56$|156)"
gu5_MO = r"(^6$|^8$|23|38|47|^50$|150)"
gu6_MO = r"(^12$|17|29|112|912)"
gu7_MO = r"(^1$|10|31|41|49|54|55$)"
gu8_MO = r"(^2$|^13$|18|21|25|34|^40$|^44$|140$)"
gu9_MO = r"(^3$|^22$|24|53$)"

msk = [gu1_M,  gu2_M, gu3_M, gu4_M,gu5_M, gu6_M, gu7_M, gu8_M, gu9_M, gu10_M]
obl = [gu1_MO,  gu2_MO, gu3_MO, gu4_MO, gu5_MO, gu6_MO, gu7_MO, gu8_MO, gu9_MO]


def search(gu_arr, current_value, out_dir):
    for i, pattern in enumerate(gu_arr):
        if re.search(pattern, current_value):
            if i == 0:
                gu_dir_name = "ГУ№1"
            else:
                gu_dir_name = "ГУ№" + str(i + 1)

            gu_path = os.path.join(out_dir, gu_dir_name)
            os.makedirs(gu_path, exist_ok=True)
            return gu_path


def get_district(current_value, out_dir, server):
    if server == "Москва":
        new_path = search(msk, current_value, out_dir)
        return new_path
    else:
        new_path = search(obl, current_value, out_dir)
        return new_path
