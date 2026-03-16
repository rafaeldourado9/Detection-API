import { ChangeEvent, useCallback, useEffect, useState } from "react";
import { listDetections, submitDetection } from "../services/api";
import { useAuth } from "../hooks/useAuth";

interface DetectedObj {
  label: string;
  confidence: number;
  bbox: { x_min: number; y_min: number; x_max: number; y_max: number };
}

interface Detection {
  id: string;
  status: string;
  image_path: string;
  objects: DetectedObj[] | null;
  created_at: string;
}

export function Dashboard() {
  const { logout } = useAuth();
  const [detections, setDetections] = useState<Detection[]>([]);
  const [uploading, setUploading] = useState(false);

  const load = useCallback(async () => {
    const data = await listDetections();
    setDetections(data);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function handleUpload(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    await submitDetection(file);
    setUploading(false);
    load();
  }

  return (
    <div className="container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Detections</h1>
        <button onClick={logout}>Logout</button>
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label>
          <strong>Upload image: </strong>
          <input type="file" accept="image/*" onChange={handleUpload} disabled={uploading} />
        </label>
        {uploading && <span> Uploading...</span>}
      </div>

      {detections.length === 0 && <p>No detections yet.</p>}

      {detections.map((d) => (
        <div key={d.id} className="card">
          <div>
            <strong>ID:</strong> {d.id.slice(0, 8)}...{" "}
            <span className={`status-${d.status}`}>{d.status}</span>
          </div>
          <div>
            <small>{new Date(d.created_at).toLocaleString()}</small>
          </div>
          {d.objects && d.objects.length > 0 && (
            <ul>
              {d.objects.map((o, i) => (
                <li key={i}>
                  {o.label} — {(o.confidence * 100).toFixed(1)}%
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}

      <button onClick={load} style={{ marginTop: "1rem" }}>
        Refresh
      </button>
    </div>
  );
}
