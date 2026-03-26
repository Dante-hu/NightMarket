let vendors = [];

async function loadVendors() {
    try {
        const res = await API.vendors.getAll();
        vendors = res.data;
        renderVendors();
    } catch (e) { console.error(e.message); }
}

function renderVendors() {
    const container = document.getElementById('vendors-list');
    if (!vendors.length) { container.innerHTML = '<div class="empty">No vendors</div>'; return; }
    container.innerHTML = vendors.map(v => `
        <div class="vendor-card" id="vendor-card-${v.vendor_id}">
            <div class="vendor-header" onclick="toggleVendor('${v.vendor_id}')">
                <div class="vendor-info">
                    <h3>${v.vendor_name}</h3>
                    <div class="meta">
                        <span class="mono id">${v.vendor_id}</span>
                        <span>NPC: ${v.npc_id}</span>
                        <span class="badge">${v.item_count} items</span>
                    </div>
                </div>
                <button onclick="event.stopPropagation(); deleteVendor('${v.vendor_id}')" class="link danger">Delete</button>
            </div>
            <div class="vendor-items" id="items-${v.vendor_id}">
                <button onclick="showAddItem('${v.vendor_id}')" class="link" style="margin-bottom: 8px; display: inline-block;">+ Add Item</button>
                <div id="add-item-form-${v.vendor_id}" class="hidden" style="margin-bottom: 8px;">
                    <div class="form-row">
                        <input id="item-id-${v.vendor_id}" class="input" placeholder="Item ID" style="width: 100px;">
                        <input id="item-name-${v.vendor_id}" class="input" placeholder="Name" style="width: 120px;">
                        <input id="item-desc-${v.vendor_id}" class="input" placeholder="Description" style="flex: 1;">
                        <input id="item-value-${v.vendor_id}" class="input" type="number" placeholder="Value" style="width: 60px;">
                        <button onclick="createItem('${v.vendor_id}')" class="btn btn-primary">Add</button>
                        <button onclick="hideAddItem('${v.vendor_id}')" class="btn">Cancel</button>
                    </div>
                </div>
                <table>
                    <thead><tr><th>ID</th><th>Name</th><th>Description</th><th>Value</th><th></th></tr></thead>
                    <tbody id="items-table-${v.vendor_id}"></tbody>
                </table>
            </div>
        </div>
    `).join('');
}

function showVendorForm() { document.getElementById('vendor-form').classList.remove('hidden'); }
function hideVendorForm() {
    document.getElementById('vendor-form').classList.add('hidden');
    ['new-vendor-id', 'new-vendor-name', 'new-vendor-node', 'new-vendor-npc'].forEach(id => document.getElementById(id).value = '');
}

async function createVendor() {
    const enteredId = document.getElementById('new-vendor-id').value.trim();
    const vendor_id = enteredId || 'v_' + Date.now();
    const vendor_name = document.getElementById('new-vendor-name').value.trim() || 'New Vendor';
    const node_id = document.getElementById('new-vendor-node').value.trim();
    const npc_id = document.getElementById('new-vendor-npc').value.trim();
    if (!node_id || !npc_id) { alert('Node ID and NPC ID required'); return; }
    try {
        await API.vendors.create({ vendor_id, vendor_name, node_id, npc_id });
        hideVendorForm();
        loadVendors();
    } catch (e) { console.error(e.message); }
}

async function deleteVendor(id) {
    if (!confirm('Delete vendor?')) return;
    try { await API.vendors.delete(id); loadVendors(); }
    catch (e) { console.error(e.message); }
}

function toggleVendor(vendorId) {
    const card = document.getElementById('vendor-card-' + vendorId);
    const items = document.getElementById('items-' + vendorId);
    if (card.classList.contains('expanded')) {
        card.classList.remove('expanded');
        items.style.display = 'none';
    } else {
        card.classList.add('expanded');
        items.style.display = 'block';
        loadVendorItems(vendorId);
    }
}

async function loadVendorItems(vendorId) {
    try {
        const res = await API.vendors.getItems(vendorId);
        const tbody = document.getElementById('items-table-' + vendorId);
        tbody.innerHTML = res.data.map(i => `
            <tr>
                <td><span class="mono" style="color: var(--accent);">${i.item_id}</span></td>
                <td><input type="text" value="${i.item_name}" onchange="updateItem('${i.item_id}', this.value, '${i.item_description}', ${i.item_value})" class="input" style="width: 100px;"></td>
                <td><input type="text" value="${i.item_description}" onchange="updateItem('${i.item_id}', '${i.item_name}', this.value, ${i.item_value})" class="input"></td>
                <td><input type="number" value="${i.item_value}" onchange="updateItem('${i.item_id}', '${i.item_name}', '${i.item_description}', parseFloat(this.value))" class="input" style="width: 60px;"></td>
                <td><button onclick="deleteItem('${i.item_id}', '${vendorId}')" class="link danger">Delete</button></td>
            </tr>
        `).join('') || '<tr><td colspan="5" class="empty">No items</td></tr>';
    } catch (e) { console.error(e.message); }
}

function showAddItem(vendorId) { document.getElementById('add-item-form-' + vendorId).classList.remove('hidden'); }
function hideAddItem(vendorId) {
    document.getElementById('add-item-form-' + vendorId).classList.add('hidden');
    ['item-id-' + vendorId, 'item-name-' + vendorId, 'item-desc-' + vendorId, 'item-value-' + vendorId].forEach(id => document.getElementById(id).value = '');
}

async function createItem(vendorId) {
    const item_id = 'i_' + Date.now();
    const item_name = 'New Item';
    const item_description = '';
    const item_value = 0;
    try {
        await API.vendors.createItem(vendorId, { item_id, item_name, item_description, item_value });
        loadVendorItems(vendorId);
        loadVendors();
    } catch (e) { console.error(e.message); }
}

async function updateItem(itemId, name, desc, value) {
    try { await API.vendors.updateItem(itemId, { item_name: name, item_description: desc, item_value: value }); }
    catch (e) { console.error(e.message); }
}

async function deleteItem(itemId, vendorId) {
    if (!confirm('Delete item?')) return;
    try {
        await API.vendors.deleteItem(itemId);
        loadVendorItems(vendorId);
        loadVendors();
    } catch (e) { console.error(e.message); }
}
