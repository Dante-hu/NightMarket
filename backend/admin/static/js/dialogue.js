let dialogueNodes = [];
let selectedNpcId = '';
let expandedNodes = new Set();
let saveTimeouts = {};

function getSiblingIndex(parentId) {
    const siblings = dialogueNodes.filter(n => n.parent_node_id === parentId);
    return siblings.length;
}

function generateNodeId(parentId) {
    const index = getSiblingIndex(parentId);
    const letter = String.fromCharCode(97 + index);
    return 'n_' + letter + '_' + Date.now();
}

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

async function loadNpcSelect() {
    try {
        const res = await API.npcs.getAll();
        document.getElementById('dialogue-npc-select').innerHTML = '<option value="">-- Select NPC --</option>' +
            res.data.map(n => `<option value="${n.npc_id}">${n.npc_name}</option>`).join('');
    } catch (e) { console.error(e.message); }
}

async function loadDialogueTree() {
    const npcId = document.getElementById('dialogue-npc-select').value;
    selectedNpcId = npcId;
    const container = document.getElementById('dialogue-tree');
    if (!npcId) { container.innerHTML = ''; return; }
    try {
        const res = await API.dialogue.getNodes(npcId);
        dialogueNodes = res.data;
        renderDialogueTree();
    } catch (e) { console.error(e.message); }
}

function renderDialogueTree() {
    const container = document.getElementById('dialogue-tree');
    if (!dialogueNodes.length) {
        container.innerHTML = `
            <div class="empty">No dialogue nodes</div>
            <button onclick="addRootNode()" class="btn btn-primary" style="margin-top: 8px;">+ Add Root Node</button>
        `;
        return;
    }
    const rootNodes = dialogueNodes.filter(n => n.parent_node_id === 'n_000');
    container.innerHTML = rootNodes.map(node => renderNode(node, 0)).join('') + 
        '<button onclick="addRootNode()" class="btn" style="margin-top: 8px;">+ Add Root Node</button>';
    
    setTimeout(() => restoreExpandedStates(), 0);
}

function restoreExpandedStates() {
    expandedNodes.forEach(nodeId => {
        const card = document.getElementById('node-card-' + nodeId);
        const content = document.getElementById('node-' + nodeId);
        if (card && content) {
            card.classList.add('expanded');
            content.style.display = 'block';
            loadOptions(nodeId);
        }
    });
}

function renderNode(node, depth) {
    const children = dialogueNodes.filter(n => n.parent_node_id === node.node_id);
    const dialogue = node.dialogue || {};
    const preview = dialogue.dialogue || '(empty)';
    const hasChildren = children.length > 0;
    const margin = Math.min(depth * 16, 48);

    return `
        <div style="margin-left: ${margin}px;">
            ${depth > 0 ? '<div style="border-left: 1px solid var(--hidden); margin-left: 8px; padding-left: 8px;">' : ''}
            <div class="node-card" id="node-card-${node.node_id}" onclick="if(event.target.closest('.node-actions') || event.target.closest('.node-content')) return; toggleNode('${node.node_id}')">
                <div class="node-header">
                    ${hasChildren ? '<span style="color: var(--subtext); font-size: 8px;">▼</span>' : '<span style="color: var(--subtext); font-size: 8px;">○</span>'}
                    <span class="mono node-id" onclick="event.stopPropagation(); copyId('${node.node_id}', event)" title="Click to copy" style="cursor:pointer;">${node.node_id}</span>
                    <span class="node-preview">${preview.substring(0, 50)}${preview.length > 50 ? '...' : ''}</span>
                    <div class="node-actions">
                        <button onclick="event.stopPropagation(); addChildNode('${node.node_id}')" class="link">+ Child</button>
                        <button onclick="event.stopPropagation(); deleteNode('${node.node_id}')" class="link danger">Delete</button>
                    </div>
                </div>
                <div class="node-content" id="node-${node.node_id}" onclick="event.stopPropagation()">
                    <div style="margin-bottom: 8px;">
                        <label style="display: block; font-size: 10px; color: var(--subtext); margin-bottom: 4px;">Dialogue</label>
                        <textarea id="dialogue-${node.node_id}" class="input" rows="2" oninput="autoSave('${node.node_id}')" placeholder="Enter dialogue...">${dialogue.dialogue || ''}</textarea>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <label style="display: block; font-size: 10px; color: var(--subtext); margin-bottom: 4px;">Translation</label>
                        <input id="translation-${node.node_id}" class="input" value="${dialogue.translation || ''}" oninput="autoSave('${node.node_id}')" placeholder="Enter translation...">
                    </div>
                    <span id="save-status-${node.node_id}" class="subtext" style="font-size: 10px;"></span>
                    <div style="margin-bottom: 4px;">
                        <button onclick="addOption('${node.node_id}')" class="link">+ Add Option</button>
                    </div>
                    <div id="options-${node.node_id}"></div>
                </div>
            </div>
            ${hasChildren ? children.map(c => renderNode(c, depth + 1)).join('') : ''}
            ${depth > 0 ? '</div>' : ''}
        </div>
    `;
}

function toggleNode(nodeId) {
    const card = document.getElementById('node-card-' + nodeId);
    const content = document.getElementById('node-' + nodeId);
    if (!card || !content) return;
    
    const isExpanded = card.classList.contains('expanded');
    if (isExpanded) {
        card.classList.remove('expanded');
        content.style.display = 'none';
        expandedNodes.delete(nodeId);
    } else {
        card.classList.add('expanded');
        content.style.display = 'block';
        loadOptions(nodeId);
        expandedNodes.add(nodeId);
    }
}

async function loadOptions(nodeId) {
    try {
        const res = await API.dialogue.getOptions(nodeId);
        const container = document.getElementById('options-' + nodeId);
        const children = dialogueNodes.filter(n => n.parent_node_id === nodeId);
        
        let nextNodeOptions = '';
        if (children.length > 0) {
            nextNodeOptions = children.map(c => `<option value="${c.node_id}">${c.node_id}</option>`).join('');
        }
        
        container.innerHTML = res.data.map(o => `
            <div style="display: flex; gap: 6px; margin-bottom: 4px; align-items: center;">
                <span class="mono" onclick="copyId('${o.option_id}', event)" title="Click to copy" style="cursor:pointer; font-size:10px; color:var(--accent);">${o.option_id}</span>
                <input type="text" id="opt-text-${o.option_id}" value="${(o.option_text || '').replace(/"/g, '&quot;')}" onchange="updateOption('${o.option_id}', this.value, getNextNodeValue('${o.option_id}'))" class="input" style="flex: 1;" placeholder="Option text...">
                <span style="color: var(--subtext); font-size: 10px;">→</span>
                ${children.length > 0 ? `
                    <select id="opt-next-sel-${o.option_id}" onchange="syncNextNode('${o.option_id}', this.value)" class="input" style="width: 100px;">
                        <option value="">-- select --</option>
                        ${nextNodeOptions}
                    </select>
                ` : ''}
                <input type="text" id="opt-next-${o.option_id}" value="${o.next_node_id || ''}" onchange="syncFromInput('${o.option_id}', this.value)" class="input" style="width: 80px;" placeholder="next node">
                <button onclick="deleteOption('${o.option_id}', '${nodeId}')" class="link danger">×</button>
            </div>
        `).join('') || '<div class="empty" style="padding: 8px;">No options</div>';
        
        res.data.forEach(o => {
            const select = document.getElementById('opt-next-sel-' + o.option_id);
            const input = document.getElementById('opt-next-' + o.option_id);
            if (select && o.next_node_id) {
                select.value = o.next_node_id;
            }
            if (select && input) {
                select.dataset.partner = 'opt-next-' + o.option_id;
                input.dataset.partner = 'opt-next-sel-' + o.option_id;
            }
        });
    } catch (e) { console.error(e.message); }
}

function getNextNodeValue(optionId) {
    const select = document.getElementById('opt-next-sel-' + optionId);
    const input = document.getElementById('opt-next-' + optionId);
    return (select && select.value) ? select.value : (input ? input.value : '');
}

function syncNextNode(optionId, value) {
    const input = document.getElementById('opt-next-' + optionId);
    if (input) input.value = value;
    const text = document.getElementById('opt-text-' + optionId).value;
    updateOption(optionId, text, value);
}

function syncFromInput(optionId, value) {
    const select = document.getElementById('opt-next-sel-' + optionId);
    if (select) {
        const hasOption = select.querySelector('option[value="' + value + '"]');
        if (hasOption) select.value = value;
    }
    const text = document.getElementById('opt-text-' + optionId).value;
    updateOption(optionId, text, value);
}

async function saveDialogue(nodeId) {
    const dialogue = document.getElementById('dialogue-' + nodeId).value;
    const translation = document.getElementById('translation-' + nodeId).value;
    expandedNodes.add(nodeId);
    await API.dialogue.updateDialogue(nodeId, { dialogue, translation });
    loadDialogueTree();
}

async function autoSave(nodeId) {
    const statusEl = document.getElementById('save-status-' + nodeId);
    statusEl.textContent = 'Saving...';
    if (saveTimeouts[nodeId]) clearTimeout(saveTimeouts[nodeId]);
    saveTimeouts[nodeId] = setTimeout(async () => {
        const dialogue = document.getElementById('dialogue-' + nodeId).value;
        const translation = document.getElementById('translation-' + nodeId).value;
        try {
            await API.dialogue.updateDialogue(nodeId, { dialogue, translation });
            statusEl.textContent = 'Saved';
            setTimeout(() => statusEl.textContent = '', 2000);
        } catch (e) {
            statusEl.textContent = 'Error saving';
        }
    }, 500);
}

async function addChildNode(parentId) {
    const nodeId = generateNodeId(parentId);
    await API.dialogue.createNode({ node_id: nodeId, parent_node_id: parentId, npc_id: selectedNpcId });
    expandedNodes.add(parentId);
    loadDialogueTree();
}

async function deleteNode(nodeId) {
    const children = dialogueNodes.filter(n => n.parent_node_id === nodeId);
    if (children.length > 0) {
        alert('Cannot delete node with child nodes. Delete child nodes first.');
        return;
    }
    if (!confirm('Delete node?')) return;
    try {
        await API.dialogue.deleteNode(nodeId);
    } catch (e) {
        alert(e.message);
        return;
    }
    expandedNodes.delete(nodeId);
    loadDialogueTree();
}

async function addRootNode() {
    const nodeId = generateNodeId('n_000');
    await API.dialogue.createNode({ node_id: nodeId, parent_node_id: 'n_000', npc_id: selectedNpcId });
    expandedNodes.add(nodeId);
    loadDialogueTree();
}

async function addOption(nodeId) {
    const optionId = 'o_' + Date.now();
    await API.dialogue.createOption(nodeId, { option_id: optionId, option_text: '', next_node_id: '', feedback_type: 'neutral' });
    expandedNodes.add(nodeId);
    loadDialogueTree();
}

async function updateOption(optionId, optionText, nextNodeId) {
    await API.dialogue.updateOption(optionId, { option_text: optionText, next_node_id: nextNodeId, feedback_type: 'neutral' });
}

async function deleteOption(optionId, nodeId) {
    if (!confirm('Delete option?')) return;
    await API.dialogue.deleteOption(optionId);
    expandedNodes.add(nodeId);
    loadDialogueTree();
}
