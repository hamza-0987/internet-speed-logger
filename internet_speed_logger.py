from speedtest import Speedtest
from datetime import datetime
from supabase_config import supabase

def bytes_to_mbps(b):
    return round(b / 1_000_000, 2)

def run_speed_test():
    st = Speedtest()
    st.get_best_server()
    download = st.download()
    upload = st.upload()
    server = st.results.server
    client = st.results.client

    result = {
        "timestamp": datetime.now().isoformat(),
        "server_name": server['name'],
        "country": server['country'],
        "sponsor": server['sponsor'],
        "ping_ms": round(server['latency'], 2),
        "download_mbps": bytes_to_mbps(download),
        "upload_mbps": bytes_to_mbps(upload),
        "client_ip": client['ip'],
        "isp": client['isp']
    }

    print("Speed test result:")
    for k, v in result.items():
        print(f"{k}: {v}")

    # Upload to Supabase
    supabase.table("internet_speed_logs").insert(result).execute()

if __name__ == "__main__":
    run_speed_test()
