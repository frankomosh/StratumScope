from datetime import datetime

def normalize(source_type, data):
    try:
        if source_type == "stratum_work":
            ntime = data.get("ntime")
            return {
                "source": "stratum_work",
                "job_id": data.get("job_id"),
                "prevhash": data.get("prev_hash"),
                "timestamp": _safe_ts(ntime or data.get("timestamp"))
            }

        elif source_type == "observer":
            return {
                "source": "observer",
                "job_id": data.get("coinbase_tag") or data.get("pool_name"),
                "prevhash": data.get("prev_hash"),
                "timestamp": _safe_ts(data.get("job_timestamp") or data.get("header_time"))
            }

    except Exception as e:
        print(f"[normalize:{source_type}] ERROR: {e}")

    return None


def _safe_ts(raw_ts):
    try:
        if not raw_ts:
            return 0.0
        if isinstance(raw_ts, (int, float)):
            return float(raw_ts)
        if isinstance(raw_ts, str):
            if raw_ts.isdigit():
                return float(raw_ts)
            # Handle hex-formatted timestamp (which is common in stratum_work)
            return float(int(raw_ts, 16))
    except:
        return 0.0
