// export const BASE_API_URL = "https://vignet-backend.glanceai.inmobi.com";
export const BASE_API_URL = "http://localhost:9000";


export function epochToJsDate(ts) {
    let dt = new Date(ts)
    return dt.toLocaleDateString() + " " + dt.toLocaleTimeString();
}