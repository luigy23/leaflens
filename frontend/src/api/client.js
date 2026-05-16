import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "";

const client = axios.create({
  baseURL,
  timeout: 30000,
});

export async function predictSpecies(file, k = 3) {
  const form = new FormData();
  form.append("image", file);
  const { data } = await client.post(`/api/predict?k=${k}`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function fetchCatalog(query = "") {
  const url = query ? `/api/species?q=${encodeURIComponent(query)}` : "/api/species";
  const { data } = await client.get(url);
  return data;
}

export async function fetchSpecies(id) {
  const { data } = await client.get(`/api/species/${id}`);
  return data;
}

export async function fetchHealth() {
  const { data } = await client.get("/api/health");
  return data;
}
