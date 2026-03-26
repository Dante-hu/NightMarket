const API = {
    async request(method, url, data = null) {
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (data) options.body = JSON.stringify(data);
        const res = await fetch(url, options);
        const json = await res.json();
        if (!res.ok) throw new Error(json.message || json.error);
        return json;
    },

    get: (url) => API.request('GET', url),
    post: (url, data) => API.request('POST', url, data),
    put: (url, data) => API.request('PUT', url, data),
    delete: (url) => API.request('DELETE', url),

    npcs: {
        getAll: () => API.get('/api/admin/npcs'),
        create: (data) => API.post('/api/admin/npcs', data),
        update: (id, data) => API.put(`/api/admin/npcs/${id}`, data),
        delete: (id) => API.delete(`/api/admin/npcs/${id}`)
    },

    dialogue: {
        getNodes: (npcId) => API.get(`/api/admin/dialogue-nodes?npc_id=${npcId}`),
        createNode: (data) => API.post('/api/admin/dialogue-nodes', data),
        updateNode: (id, data) => API.put(`/api/admin/dialogue-nodes/${id}`, data),
        deleteNode: (id) => API.delete(`/api/admin/dialogue-nodes/${id}`),
        getDialogue: (nodeId) => API.get(`/api/admin/dialogues/${nodeId}`),
        updateDialogue: (nodeId, data) => API.put(`/api/admin/dialogues/${nodeId}`, data),
        getOptions: (nodeId) => API.get(`/api/admin/options/${nodeId}`),
        createOption: (nodeId, data) => API.post(`/api/admin/options/${nodeId}`, data),
        updateOption: (id, data) => API.put(`/api/admin/options/${id}`, data),
        deleteOption: (id) => API.delete(`/api/admin/options/${id}`)
    },

    vendors: {
        getAll: () => API.get('/api/admin/vendors'),
        create: (data) => API.post('/api/admin/vendors', data),
        update: (id, data) => API.put(`/api/admin/vendors/${id}`, data),
        delete: (id) => API.delete(`/api/admin/vendors/${id}`),
        getItems: (vendorId) => API.get(`/api/admin/items/${vendorId}`),
        createItem: (vendorId, data) => API.post(`/api/admin/items/${vendorId}`, data),
        updateItem: (id, data) => API.put(`/api/admin/items/${id}`, data),
        deleteItem: (id) => API.delete(`/api/admin/items/${id}`)
    }
};
