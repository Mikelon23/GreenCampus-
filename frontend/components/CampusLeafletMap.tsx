import L from "leaflet";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

export type MapZone = {
  id: number;
  name: string;
  description?: string | null;
  location_coordinates?: string | null;
};

export type MapSensor = {
  zone_id: number;
  temperature: number;
  humidity: number;
  co2_level: number;
};

export type SmartBin = {
  id: number;
  name: string;
  position: [number, number];
};

type CampusLeafletMapProps = {
  zones: MapZone[];
  zoneMetrics: Record<number, MapSensor>;
  smartBins: SmartBin[];
  userSignedIn: boolean;
  recyclingBusy: string | null;
  onRecycle: (material: "plastic" | "paper" | "glass") => void;
};

const CAMPUS_CENTER: [number, number] = [-1.6598, -78.6780];

const sensorIcon = L.divIcon({
  className: "",
  html: '<div style="height:18px;width:18px;border-radius:9999px;background:#2f855a;border:3px solid white;box-shadow:0 8px 18px rgba(0,0,0,.25)"></div>',
  iconSize: [18, 18],
  iconAnchor: [9, 9]
});

const binIcon = L.divIcon({
  className: "",
  html: '<div style="height:20px;width:20px;border-radius:6px;background:#2f80ed;border:3px solid white;box-shadow:0 8px 18px rgba(0,0,0,.25)"></div>',
  iconSize: [20, 20],
  iconAnchor: [10, 10]
});

function zonePosition(zone: MapZone, index: number): [number, number] {
  const [lat, lng] = (zone.location_coordinates || "")
    .split(",")
    .map((value) => Number(value.trim()));

  if (Number.isFinite(lat) && Number.isFinite(lng) && Math.abs(lat) > 0.001 && Math.abs(lng) > 0.001) {
    return [lat, lng];
  }

  // Major change: zones without coordinates receive stable demo positions around a generic campus center.
  const offsets: [number, number][] = [
    [0.0012, -0.001],
    [0.001, 0.0011],
    [-0.0011, 0.0009],
    [-0.0012, -0.001],
    [0.0002, 0.0017],
    [-0.0002, -0.0018]
  ];
  const offset = offsets[index % offsets.length];
  return [CAMPUS_CENTER[0] + offset[0], CAMPUS_CENTER[1] + offset[1]];
}

export default function CampusLeafletMap({
  zones,
  zoneMetrics,
  smartBins,
  userSignedIn,
  recyclingBusy,
  onRecycle
}: CampusLeafletMapProps) {
  return (
    <MapContainer center={CAMPUS_CENTER} zoom={16} scrollWheelZoom className="h-full w-full">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {zones.map((zone, index) => {
        const metric = zoneMetrics[zone.id];
        return (
          <Marker key={zone.id} position={zonePosition(zone, index)} icon={sensorIcon}>
            <Popup>
              <div className="space-y-1 text-sm">
                <p className="font-semibold">{zone.name}</p>
                <p>{zone.description || "Environmental ESP32 sensor"}</p>
                {metric ? (
                  <>
                    <p>Temp: {metric.temperature.toFixed(1)} C</p>
                    <p>Humidity: {metric.humidity.toFixed(1)}%</p>
                    <p>CO2: {metric.co2_level.toFixed(0)} ppm</p>
                  </>
                ) : (
                  <p>No sensor data yet.</p>
                )}
              </div>
            </Popup>
          </Marker>
        );
      })}

      {smartBins.map((bin) => (
        <Marker key={bin.id} position={bin.position} icon={binIcon}>
          <Popup>
            <div className="space-y-3 text-sm">
              <div>
                <p className="font-semibold">{bin.name}</p>
                <p>Smart recycling bin</p>
              </div>
              <div className="flex flex-col gap-2">
                {(["plastic", "paper", "glass"] as const).map((material) => (
                  <button
                    key={material}
                    type="button"
                    disabled={!userSignedIn || recyclingBusy === material}
                    onClick={() => onRecycle(material)}
                    className="rounded-lg bg-campus-700 px-3 py-2 text-xs font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {recyclingBusy === material ? "Saving..." : `Simular ${material}`}
                  </button>
                ))}
              </div>
              {!userSignedIn ? <p className="text-xs text-slate-500">Sign in to earn Green Points.</p> : null}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
