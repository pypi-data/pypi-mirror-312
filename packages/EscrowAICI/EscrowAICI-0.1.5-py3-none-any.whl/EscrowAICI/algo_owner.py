import requests
from EscrowAICI import general
import sseclient
import os
import json
from azure.storage.blob import BlobClient
from EscrowAICI.utils import generate_frontoffice_url, generate_notifications_url


def upload_algo(
    env,
    project,
    org,
    name,
    version_description,
    compute,
    memory,
    machine,
    type,
    file,
    token,
    algorithm_description,
):
    try:
        artifacts = find_artifacts(env, project, type, token)
        attest = artifacts[0]
        valid = artifacts[1]
        wkey = find_wkey(env, project, token)
        baseUrl = generate_frontoffice_url(environment=env)

        if compute == "Intel SGX":
            response = requests.post(
                f"{baseUrl}/composite/algorithm/",
                headers={"Authorization": "Bearer " + token},
                data={
                    "algorithm": '"{\\"name\\":\\"'
                    + name
                    + '\\",\\"description\\":\\"'
                    + algorithm_description
                    + '\\",\\"project\\":\\"'
                    + project
                    + '\\",\\"organization\\":\\"'
                    + org
                    + '\\"}"',
                    "version_tag": "v1",
                    "description": version_description,
                    "algorithm_type": type,
                    "validation_criteria_version": valid,
                    "data_attestation_version": attest,
                    "has_phi_agreement": "true",
                    "upload_file_name": os.path.basename(file),
                    "upload_type": "Upload Zip",
                    "wcek_version": wkey,
                    "sgx_memory": memory,
                    "machine_type": machine,
                    "is_fortanix_sgx_enabled": "true",
                    "is_microsoft_aci_enabled": "false",
                    "is_cvm_enabled": "false",
                },
                files=[("0", (file, open(file, "rb"), "application/zip"))],
            )
        if compute == "Microsoft ACI":
            response = requests.post(
                f"{baseUrl}/composite/algorithm/",
                headers={"Authorization": "Bearer " + token},
                data={
                    "algorithm": '"{\\"name\\":\\"'
                    + name
                    + '\\",\\"description\\":\\"'
                    + algorithm_description
                    + '\\",\\"project\\":\\"'
                    + project
                    + '\\",\\"organization\\":\\"'
                    + org
                    + '\\"}"',
                    "version_tag": "v1",
                    "description": version_description,
                    "algorithm_type": type,
                    "validation_criteria_version": valid,
                    "data_attestation_version": attest,
                    "has_phi_agreement": "true",
                    "upload_file_name": os.path.basename(file),
                    "upload_type": "Upload Zip",
                    "wcek_version": wkey,
                    "is_fortanix_sgx_enabled": "false",
                    "is_microsoft_aci_enabled": "true",
                    "is_cvm_enabled": "false",
                },
                files=[("0", (file, open(file, "rb"), "application/zip"))],
            )
        if compute == "CVM":
            response = requests.post(
                f"{baseUrl}/composite/algorithm/",
                headers={"Authorization": "Bearer " + token},
                data={
                    "algorithm": '"{\\"name\\":\\"'
                    + name
                    + '\\",\\"description\\":\\"'
                    + algorithm_description
                    + '\\",\\"project\\":\\"'
                    + project
                    + '\\",\\"organization\\":\\"'
                    + org
                    + '\\"}"',
                    "version_tag": "v1",
                    "description": version_description,
                    "algorithm_type": type,
                    "validation_criteria_version": valid,
                    "data_attestation_version": attest,
                    "has_phi_agreement": "true",
                    "upload_type": "Upload Zip",
                    "upload_file_name": os.path.basename(file),
                    "wcek_version": wkey,
                    "is_fortanix_sgx_enabled": "false",
                    "is_microsoft_aci_enabled": "false",
                    "is_cvm_enabled": "true",
                },
                files=[("0", (file, open(file, "rb"), "application/zip"))],
            )

        return response
    except Exception as e:
        print("Error uploading Algorithm to escrow")
        print(e)
        raise (e)


def upload_algo_version(
    env, project, algo_id, version, description, compute, type, file, token
):
    baseUrl = generate_frontoffice_url(environment=env)
    sgx = False
    aci = False
    cvm = False
    if compute == "Intel SGX":
        sgx = True
    if compute == "Microsoft ACI":
        aci = True
    if compute == "CVM":
        cvm = True

    artifacts = find_artifacts(env, project, type, token)
    attest = artifacts[0]
    valid = artifacts[1]
    wkey = find_wkey(env, project, token)

    algo_get = requests.get(
        f"{baseUrl}/algorithm/{algo_id}/",
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + token,
            "User-Agent": "curl/7.71.1",
        },
    )
    if algo_get.status_code != 200:
        return algo_get

    try:
        response = requests.post(
            f"{baseUrl}/algorithm-version/",
            headers={
                "Authorization": "Bearer " + token,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
            },
            data={
                "algorithm": algo_id,
                "version_tag": version,
                "description": description,
                "algorithm_type": type,
                "validation_criteria_version": valid,
                "data_attestation_version": attest,
                "upload_type": "Upload Zip",
                "upload_file_name": os.path.basename(file),
                "has_phi_agreement": "true",
                "wcek_version": wkey,
                "is_fortanix_sgx_enabled": str(sgx),
                "is_microsoft_aci_enabled": str(aci),
                "is_cvm_enabled": str(cvm),
            },
            files=[("0", (file, open(file, "rb"), "application/zip"))],
        )

        return response
    except Exception as e:
        print("Error uploading algo version to Escrow")
        print(e)
        raise (e)


def finish_algo_upload(env, file, response, algo_id, compute, token):
    try:
        baseUrl = generate_frontoffice_url(environment=env)
        sgx = False
        aci = False
        cvm = False
        if compute == "Intel SGX":
            sgx = True
        if compute == "Microsoft ACI":
            aci = True
        if compute == "CVM":
            cvm = True
        data = response.json()

        version_id = data["algorithm_version_id"]
        url = data["upload_url"]
        client = BlobClient.from_blob_url(url)

        with open(file, "rb") as upload:
            client.upload_blob(upload, overwrite=True)

        patch = requests.patch(
            f"{baseUrl}/algorithm-version/{version_id}/",
            headers={"Authorization": "Bearer " + token, "User-Agent": "curl/7.71.1"},
            data={
                "status": "In Progress",
                "algorithm": algo_id,
                "is_fortanix_sgx_enabled": str(sgx),
                "is_microsoft_aci_enabled": str(aci),
                "is_cvm_enabled": str(cvm),
            },
            files=[("0", (file, open(file, "rb"), "application/zip"))],
        )

        return patch
    except Exception as e:
        print("Error uploading algorithm details")
        print(e)
        raise (e)


def get_algo_notification(env, project, compute, token):
    baseNotificationsUrl = generate_notifications_url(environment=env)
    client = sseclient.SSEClient(
        f"{baseNotificationsUrl}/project-notifications/{project}/?token={token}"
    )
    docker = False
    if compute == "Intel SGX":
        enclave = False
    else:
        enclave = True
    for event in client:
        if event.event != "stream-open" and event.event != "keep-alive":
            if event.data != "":
                message = json.loads(event.data)["message"]
                print(f"\033[1m\033[92mESCROWAI: \033[0m\033[0m{message}")
                if message == "Docker Push Succeeded":
                    docker = True
                if message == "EnclaveOS Build Succeded":
                    enclave = True
                if docker and enclave:
                    return True
                if (
                    message == "File Validation Failed"
                    or message == "EnclaveOS Build Failed"
                ):
                    return False


def upload_run_config(
    env,
    project,
    name,
    description,
    algo_version,
    ds_version,
    compute,
    memory,
    type,
    token,
):
    baseUrl = generate_frontoffice_url(environment=env)
    versions = general.find_algo_ds_versions(
        env, project, algo_version, ds_version, token
    )

    response = requests.post(
        f"{baseUrl}/run-configuration/",
        headers={"Authorization": "Bearer " + token, "User-Agent": "curl/7.71.1"},
        data={
            "algorithm_version": versions[0],
            "dataset_version": versions[1],
            "project": project,
            "name": name,
            "description": description,
            "test_type": "Regular",
            "run_type": type,
            "confidential_compute_technology": compute,
            "algo_container_memory": memory,
        },
    )

    return response


def send_notification(
    env,
    project,
    algo_version,
    ds_version,
    memory,
    machines,
    machine,
    training_parameters,
    token,
):
    baseUrl = generate_frontoffice_url(environment=env)
    rc = general.find_run_config(env, project, algo_version, ds_version, token)

    if machine == "":
        response = requests.post(
            f"{baseUrl}/algorithm-version/{rc}/run/",
            headers={"Authorization": "Bearer " + token, "User-Agent": "curl/7.71.1"},
            data={
                "run_timeout": 30,
                "algo_container_cpus": machines,
                "algo_container_memory": memory,
                "run_configuration": rc,
                "training_parameters": training_parameters,
            },
        )
    else:
        response = requests.post(
            f"{baseUrl}/algorithm-version/{rc}/run/",
            headers={"Authorization": "Bearer " + token, "User-Agent": "curl/7.71.1"},
            data={
                "run_timeout": 30,
                "run_configuration": rc,
                "machine_type": machine,
                "training_parameters": training_parameters,
            },
        )

    return response


def download_report(env, project, token):
    baseUrl = generate_frontoffice_url(environment=env)
    configs = requests.get(
        f"{baseUrl}/run-configuration/?project_id={project}",
        headers={"Authorization": "Bearer " + token, "User-Agent": "curl/7.71.1"},
    )

    if configs.status_code != 200:
        print("\033[1m\033[36mCLIENT:\033[0m\033[0m ERROR: ", configs.status_code)
        print(configs.text)
        return False

    config_id = configs.json()[0]["id"]

    report_response = requests.get(
        f"{baseUrl}/report/?run_configuration={config_id}",
        headers={"User-Agent": "curl/7.71.1", "Authorization": "Bearer " + token},
    )

    if report_response.status_code == 200:
        output = report_response.json()[0]["json_data"][12:-2]
        f = open("downloads/report.txt", "w")
        f.write(output)
        f.close()

    return report_response


def find_artifacts(env, project, type, token):
    baseUrl = generate_frontoffice_url(environment=env)
    artifact_get = requests.get(
        f"{baseUrl}/artifact/?project_id={project}",
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + token,
            "User-Agent": "curl/7.71.1",
        },
    )

    ajs = artifact_get.json()

    data_attestation_artifact_id = None
    validation_criteria_artifact_id = None

    for i in ajs:
        if (
            i.get("artifact_type")
            and i.get("artifact_type").get("name") == "validation_criteria"
        ):
            validation_criteria_artifact_id = i["id"]
        if (
            i.get("artifact_type")
            and i.get("artifact_type").get("name") == "data_attestation"
        ):
            data_attestation_artifact_id = i["id"]

    if not data_attestation_artifact_id:
        raise Exception("Could not find a Data Attestation artifact on the project")

    if not validation_criteria_artifact_id and type == "validation":
        raise Exception("Could not find a Validation Criteria artifact on the project")

    artifact_v_get = requests.get(
        f"{baseUrl}/artifact-version/?artifact_id={data_attestation_artifact_id}",
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + token,
            "User-Agent": "curl/7.71.1",
        },
    )
    attest_id = artifact_v_get.json()[0]["id"]

    valid_id = None
    if type == "validation":
        artifact_v_get = requests.get(
            f"{baseUrl}/artifact-version/?artifact_id={validation_criteria_artifact_id}",
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + token,
                "User-Agent": "curl/7.71.1",
            },
        )
        valid_id = artifact_v_get.json()[0]["id"]

    return attest_id, valid_id


def find_wkey(env, project, token):
    return general.find_keys(env, project, True, token)[2]
