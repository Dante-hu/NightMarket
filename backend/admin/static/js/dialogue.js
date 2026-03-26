let dialogueNodes = [];
let selectedNpcId = '';
let expandedNodes = new Set();

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
    
    // Restore expanded states
    setTimeout(() => restoreExpandedStates(), 0);
}

function restoreExpandedStates() {
    expandedNodes.forEach(nodeId => {
        const card = document.getElementById('node-card-' + nodeId);
        const content = document.getElementById('node-' + nodeId);
        const children = document.getElementById('children-' + nodeId);
        if (card && content) {
            card.classList.add('expanded');
            content.style.display = 'block';
            if (children) children.style.display = 'block';
            // Load options for expanded nodes
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
                    ${hasChildren ? '<span style="color: var(--subtext);">▶</span>' : ''}
                    <span class="mono node-id">${node.node_id}</span>
                    <span class="node-preview">${preview.substring(0, 50)}${preview.length > 50 ? '...' : ''}</span>
                    <div class="node-actions">
                        <button onclick="event.stopPropagation(); addChildNode('${node.node_id}')" class="link">+ Child</button>
                        <button onclick="event.stopPropagation(); deleteNode('${node.node_id}')" class="link danger">Delete</button>
                    </div>
                </div>
                <div class="node-content" id="node-${node.node_id}" onclick="event.stopPropagation()">
                    <div style="margin-bottom: 8px;">
                        <label style="display: block; font-size: 10px; color: var(--subtext); margin-bottom: 4px;">Dialogue</label>
                        <textarea id="dialogue-${node.node_id}" class="input" rows="2" onclick="event.stopPropagation()">${dialogue.dialogue || ''}</textarea>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <label style="display: block; font-size: 10px; color: var(--subtext); margin-bottom: 4px;">Translation</label>
                        <input id="translation-${node.node_id}" class="input" value="${dialogue.translation || ''}" onclick="event.stopPropagation()">
                    </div>
                    <button onclick="saveDialogue('${node.node_id}')" class="btn" style="margin-bottom: 8px;">Save</button>
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
        container.innerHTML = res.data.map(o => `
            <div style="display: flex; gap: 6px; margin-bottom: 4px; align-items: center;">
                <input type="text" id="opt-text-${o.option_id}" value="${(o.option_text || '').replace(/"/g, '&quot;')}" onchange="updateOption('${o.option_id}', this.value, document.getElementById('opt-next-${o.option_id}').value)" class="input" style="flex: 1;" placeholder="Option text...">
                <span style="color: var(--subtext); font-size: 10px;">→</span>
                <input type="text" id="opt-next-${o.option_id}" value="${o.next_node_id || ''}" onchange="updateOption('${o.option_id}', document.getElementById('opt-text-${o.option_id}').value, this.value)" class="input" style="width: 80px;" placeholder="next node">
                <button onclick="deleteOption('${o.option_id}', '${nodeId}')" class="link danger">×</button>
            </div>
        `).join('') || '<div class="empty" style="padding: 8px;">No options</div>';
    } catch (e) { console.error(e.message); }
}

async function saveDialogue(nodeId) {
    const dialogue = document.getElementById('dialogue-' + nodeId).value;
    const translation = document.getElementById('translation-' + nodeId).value;
    expandedNodes.add(nodeId);
    await API.dialogue.updateDialogue(nodeId, { dialogue, translation });
    loadDialogueTree();
}

async function addChildNode(parentId) {
    const existingIds = dialogueNodes.map(n => n.node_id);
    let nodeId = 'n_' + Date.now();
    let counter = 1;
    while (existingIds.includes(nodeId)) {
        nodeId = 'n_' + Date.now() + '_' + counter++;
    }
    await API.dialogue.createNode({ node_id: nodeId, parent_node_id: parentId, npc_id: selectedNpcId });
    expandedNodes.add(parentId);
    loadDialogueTree();
}

async function deleteNode(nodeId) {
    // Check if node has children
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
    const existingIds = dialogueNodes.map(n => n.node_id);
    let nodeId = 'n_' + Date.now();
    let counter = 1;
    while (existingIds.includes(nodeId)) {
        nodeId = 'n_' + Date.now() + '_' + counter++;
    }
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
