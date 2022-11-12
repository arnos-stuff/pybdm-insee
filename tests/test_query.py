from pybdm_insee.tools.insee import (
    process_xml_output, _insee_idb_data_url,
    insee_get_access_token, insee_bdm_get,
    process_xml_output
)


obj = process_xml_output(insee_bdm_get("001656506"))

for val in obj["series"]:
    print(val)

print(obj["metadata"])