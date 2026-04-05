let npcs = [];
let allDialogueNodes = [];

function copyId(text, event) {
    navigator.clipboard.writeText(text);
    const el = event.target;
    const original = el.textContent;
    el.textContent = 'Copied!';
    el.style.color = 'var(--green)';
    setTimeout(() => {
        el.textContent = original;
        el.style.color = '';
    }, 1000);
}

async function loadNpcs() {
    try {
        const [npcsRes, dialogueRes] = await Promise.all([
            API.npcs.getAll(),
            Promise.all((await API.npcs.getAll()).data.map(n => API.dialogue.getNodes(n.npc_id)))
        ]);
        npcs = npcsRes.data;
        allDialogueNodes = dialogueRes.flatMap(d => d.data);
        renderNpcTable();
    } catch (e) { console.error(e.message); }
}

function renderNpcTable() {
    const tbody = document.getElementById('npc-table-body');
    if (!npcs.length) {
        tbody.innerHTML = '<tr><td colspan="3" class="empty">No NPCs</td></tr>';
        return;
    }
    tbody.innerHTML = npcs.map(npc => `
        <tr>
            <td><span class="mono id" onclick="copyId('${npc.npc_id}', event)" title="Click to copy" style="cursor:pointer;">${npc.npc_id}</span></td>
            <td><input type="text" value="${npc.npc_name}" onchange="updateNpc('${npc.npc_id}', this.value)" class="input" style="max-width: 200px;"></td>
            <td><button onclick="deleteNpc('${npc.npc_id}')" class="link danger">Delete</button></td>
        </tr>
    `).join('');
}

function showNpcForm() { document.getElementById('npc-form').classList.remove('hidden'); }
function hideNpcForm() {
    document.getElementById('npc-form').classList.add('hidden');
    document.getElementById('new-npc-id').value = '';
    document.getElementById('new-npc-name').value = '';
}

async function createNpc() {
    const enteredId = document.getElementById('new-npc-id').value.trim();
    const id = enteredId || 'npc_' + Date.now();
    const name = document.getElementById('new-npc-name').value.trim();
    if (!name) {
        alert('Name is required');
        return;
    }
    try {
        await API.npcs.create({ npc_id: id, npc_name: name });
        hideNpcForm();
        loadNpcs();
    } catch (e) { console.error(e.message); }
}

async function updateNpc(id, name) {
    try { await API.npcs.update(id, { npc_name: name }); }
    catch (e) { console.error(e.message); loadNpcs(); }
}

async function deleteNpc(id) {
    const hasNodes = allDialogueNodes.some(n => n.npc_id === id);
    if (hasNodes) {
        alert('Cannot delete NPC with existing dialogue nodes. Delete dialogue nodes first.');
        return;
    }
    if (!confirm('Delete this NPC?')) return;
    try { await API.npcs.delete(id); loadNpcs(); }
    catch (e) { alert(e.message); }
}
