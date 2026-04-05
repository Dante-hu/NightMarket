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
    const audioBinary = dialogue.audio_src?.audio_binary;
    const hasAudio = audioBinary && audioBinary.length > 0;
    const audioSrc = hasAudio ? `data:audio/wav;base64,${audioBinary}` : '';
    
    function esc(str) {
        if (!str) return '';
        return String(str).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, '\\n');
    }
    
    const dialogueText = esc(dialogue.dialogue);
    const translationText = esc(dialogue.translation_HAN);
    const translationPOJ = esc(dialogue.translation_POJ);
    const nodeId = esc(node.node_id);

    return `
        <div style="margin-left: ${margin}px;">
            ${depth > 0 ? '<div style="border-left: 1px solid var(--hidden); margin-left: 8px; padding-left: 8px;">' : ''}
            <div class="node-card" id="node-card-${node.node_id}" onclick="if(event.target.closest('.node-actions') || event.target.closest('.node-content')) return; toggleNode('${node.node_id}')">
                <div class="node-header">
                    ${hasChildren ? '<span style="color: var(--subtext); font-size: 8px;">▼</span>' : '<span style="color: var(--subtext); font-size: 8px;">○</span>'}
                    <span class="mono node-id" onclick="event.stopPropagation(); copyId('${node.node_id}', event)" title="Click to copy" style="cursor:pointer;">${node.node_id}</span>
                    <span class="node-preview">${preview.substring(0, 50)}${preview.length > 50 ? '...' : ''}</span>
                    <span id="save-status-${node.node_id}" class="subtext" style="font-size: 10px; margin-left: auto; min-width: 60px; text-align: right;"></span>
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
                        <input id="translation-${node.node_id}-HAN" class="input" value="${dialogue.translation_HAN || ''}" oninput="autoSave('${node.node_id}')" placeholder="Enter HAN translation...">
                        <button onclick="generateTranslations(document.getElementById('dialogue-${node.node_id}').value,'${node.node_id}','HAN')" class="gen-btn">Generate Translations</button>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <label style="display: block; font-size: 10px; color: var(--subtext); margin-bottom: 4px;">Translation</label>
                        <input id="translation-${node.node_id}-POJ" class="input" value="${dialogue.translation_POJ || ''}" oninput="autoSave('${node.node_id}')" placeholder="Enter POJ translation...">
                        <button onclick="generateTranslations(document.getElementById('dialogue-${node.node_id}').value,'${node.node_id}','POJ')" class="gen-btn">Generate Translations</button>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <label style="display: block; font-size: 10px; color: var(--subtext); margin-bottom: 4px;">Audio</label>
                        ${hasAudio ? `
                        <div class="audio-player" data-node-id="${nodeId}">
                            <button class="audio-play-btn" onclick="toggleAudio(this, '${nodeId}')"></button>
                            <span class="audio-time">0:00</span>
                            <div class="audio-progress" onmousedown="startSeek(event, this, '${nodeId}')">
                                <div class="audio-progress-fill"></div>
                            </div>
                            <span class="audio-time">0:00</span>
                            <div class="audio-volume">
                                <button class="audio-volume-btn" onclick="toggleMute(this, '${node.node_id}')"></button>
                                <div class="audio-volume-slider" onmousedown="startVolume(event, this, '${node.node_id}')">
                                    <div class="audio-volume-fill"></div>
                                </div>
                            </div>
                        </div>
                        <audio id="audio-${node.node_id}" preload="metadata" style="display: none;">
                            <source src="${audioSrc}" type="audio/wav">
                        </audio>
                        ` : `
                        <span class="subtext" style="font-size: 10px; display: block; margin-bottom: 6px;">No audio generated</span>
                        `}
                        <button onclick="generateTTS(document.getElementById('translation-${node.node_id}-POJ').value,'${nodeId}')" class="gen-btn">Generate Audio</button>
                    </div>
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
    const translationHAN = document.getElementById('translation-' + nodeId + '-HAN').value;
    const translationPOJ = document.getElementById('translation-' + nodeId + '-POJ').value;
    expandedNodes.add(nodeId);
    await API.dialogue.updateDialogue(nodeId, { dialogue, translationHAN, translationPOJ });
    loadDialogueTree();
}

async function autoSave(nodeId) {
    const statusEl = document.getElementById('save-status-' + nodeId);
    statusEl.textContent = 'Saving...';
    if (saveTimeouts[nodeId]) clearTimeout(saveTimeouts[nodeId]);
    saveTimeouts[nodeId] = setTimeout(async () => {
        const dialogue = document.getElementById('dialogue-' + nodeId).value;
        const translationHAN = document.getElementById('translation-' + nodeId + '-HAN').value;
        const translationPOJ = document.getElementById('translation-' + nodeId + '-POJ').value;

        try {
            await API.dialogue.updateDialogue(nodeId, { dialogue, translationHAN, translationPOJ });
            statusEl.textContent = 'Saved';
            setTimeout(() => { if (statusEl.textContent === 'Saved') statusEl.textContent = ''; }, 2000);
        } catch (e) {
            statusEl.textContent = 'Error';
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

async function generateTranslations(dialogueText, nodeId, targetLang){
    console.log("[generateTranslations] dialogueText:", dialogueText, "nodeId:", nodeId, "targetLang:", targetLang);
    const statusEl = document.getElementById('save-status-' + nodeId);
    const btnEl = event.target;
    if (!dialogueText || dialogueText == "") { 
        alert("Please enter dialogue text first");
        return 
    }
    try {
        btnEl.classList.add('loading');
        btnEl.disabled = true;
        btnEl.textContent = 'Generating...';
        statusEl.textContent = 'Translating...';
        await API.model.translate(nodeId, { output_lang: targetLang, input_text: dialogueText });
        statusEl.textContent = 'Done';
        btnEl.classList.add('success');
        btnEl.textContent = 'Generated';
    } catch (e) {
        console.log(e) 
        statusEl.textContent = 'Error';
        btnEl.classList.add('error');
        btnEl.textContent = 'Failed';
    } finally {
        btnEl.classList.remove('loading');
        btnEl.disabled = false;
        setTimeout(() => {
            btnEl.classList.remove('error', 'success');
            btnEl.textContent = 'Generate Translations';
        }, 2000);
    }
    loadDialogueTree();
}

async function generateTTS(translatedText, nodeId){
    console.log("[generateTTS] translatedText:", translatedText, "nodeId:", nodeId);
    const statusEl = document.getElementById('save-status-' + nodeId);
    const btnEl = event.target;
    if (!translatedText || translatedText == "") { 
        alert("Please generate a translation first");
        return 
    }
    try {
        btnEl.classList.add('loading');
        btnEl.disabled = true;
        btnEl.textContent = 'Generating...';
        statusEl.textContent = 'Generating...';
        await API.model.tts(nodeId, { translation_text: translatedText });
        statusEl.textContent = 'Done';
        btnEl.classList.add('success');
        btnEl.textContent = 'Generated';
    } catch (e) {
        console.log(e) 
        statusEl.textContent = 'Error';
        btnEl.classList.add('error');
        btnEl.textContent = 'Failed';
    } finally {
        btnEl.classList.remove('loading');
        btnEl.disabled = false;
        setTimeout(() => {
            btnEl.classList.remove('error', 'success');
            btnEl.textContent = 'Generate Audio';
        }, 2000);
    }
    loadDialogueTree();
}

function toggleAudio(btn, nodeId) {
    const audio = document.getElementById('audio-' + nodeId);
    const player = btn.closest('.audio-player');
    if (!audio || !player) return;
    
    if (audio.paused) {
        document.querySelectorAll('.audio-play-btn.playing').forEach(b => {
            const otherAudio = document.getElementById('audio-' + b.closest('.audio-player').dataset.nodeId);
            if (otherAudio) { otherAudio.pause(); otherAudio.currentTime = 0; }
            b.classList.remove('playing');
        });
        audio.play();
        btn.classList.add('playing');
        audio.addEventListener('timeupdate', () => updateAudioProgress(nodeId));
        audio.addEventListener('ended', () => {
            btn.classList.remove('playing');
            const fill = player.querySelector('.audio-progress-fill');
            const timeEl = player.querySelectorAll('.audio-time');
            if (fill) fill.style.width = '0%';
            if (timeEl[0]) timeEl[0].textContent = '0:00';
            if (timeEl[1]) timeEl[1].textContent = formatTime(audio.duration);
        });
        if (isNaN(audio.duration)) {
            audio.addEventListener('loadedmetadata', () => {
                const timeEl = player.querySelectorAll('.audio-time');
                if (timeEl[1]) timeEl[1].textContent = formatTime(audio.duration);
            }, { once: true });
        } else {
            const timeEl = player.querySelectorAll('.audio-time');
            if (timeEl[1]) timeEl[1].textContent = formatTime(audio.duration);
        }
    } else {
        audio.pause();
        btn.classList.remove('playing');
    }
}

function updateAudioProgress(nodeId) {
    const audio = document.getElementById('audio-' + nodeId);
    const player = document.querySelector(`.audio-player[data-node-id="${nodeId}"]`);
    if (!audio || !player) return;
    
    const fill = player.querySelector('.audio-progress-fill');
    const timeEl = player.querySelectorAll('.audio-time');
    const progress = (audio.currentTime / audio.duration) * 100;
    
    if (fill) fill.style.width = progress + '%';
    if (timeEl[0]) timeEl[0].textContent = formatTime(audio.currentTime);
}

let isSeeking = false;
let seekNodeId = null;

function startSeek(event, progressEl, nodeId) {
    isSeeking = true;
    seekNodeId = nodeId;
    seekAudio(event, progressEl, nodeId);
    document.addEventListener('mousemove', onSeek);
    document.addEventListener('mouseup', stopSeek);
}

function onSeek(event) {
    if (!isSeeking || !seekNodeId) return;
    const progressEl = document.querySelector(`.audio-player[data-node-id="${seekNodeId}"] .audio-progress`);
    if (progressEl) seekAudio(event, progressEl, seekNodeId);
}

function stopSeek() {
    isSeeking = false;
    seekNodeId = null;
    document.removeEventListener('mousemove', onSeek);
    document.removeEventListener('mouseup', stopSeek);
}

function seekAudio(event, progressEl, nodeId) {
    const audio = document.getElementById('audio-' + nodeId);
    if (!audio) return;
    
    const rect = progressEl.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    audio.currentTime = percent * audio.duration;
    
    const fill = progressEl.querySelector('.audio-progress-fill');
    if (fill) fill.style.width = (percent * 100) + '%';
}

let isVolumeDrag = false;
let volumeNodeId = null;
let volumeStartX = 0;
let volumeStartPercent = 0;

function startVolume(event, sliderEl, nodeId) {
    isVolumeDrag = true;
    volumeNodeId = nodeId;
    const rect = sliderEl.getBoundingClientRect();
    volumeStartX = event.clientX;
    volumeStartPercent = (event.clientX - rect.left) / rect.width;
    setVolume(event, sliderEl, nodeId);
    document.addEventListener('mousemove', onVolumeDrag);
    document.addEventListener('mouseup', stopVolumeDrag);
}

function onVolumeDrag(event) {
    if (!isVolumeDrag || !volumeNodeId) return;
    const sliderEl = document.querySelector(`.audio-player[data-node-id="${volumeNodeId}"] .audio-volume-slider`);
    if (sliderEl) {
        const rect = sliderEl.getBoundingClientRect();
        const deltaX = event.clientX - volumeStartX;
        const deltaPercent = deltaX / rect.width;
        let newPercent = volumeStartPercent + deltaPercent;
        newPercent = Math.max(0, Math.min(1, newPercent));
        
        const audio = document.getElementById('audio-' + volumeNodeId);
        if (audio) {
            audio.volume = newPercent;
            audio.dataset.volume = newPercent;
        }
        
        const fill = sliderEl.querySelector('.audio-volume-fill');
        if (fill) {
            fill.style.width = (newPercent * 100) + '%';
        }
        
        const volBtn = sliderEl.parentElement.querySelector('.audio-volume-btn');
        if (volBtn) volBtn.classList.toggle('muted', newPercent === 0);
    }
}

function stopVolumeDrag() {
    isVolumeDrag = false;
    volumeNodeId = null;
    document.removeEventListener('mousemove', onVolumeDrag);
    document.removeEventListener('mouseup', stopVolumeDrag);
}

function setVolume(event, sliderEl, nodeId) {
    const audio = document.getElementById('audio-' + nodeId);
    if (!audio) return;
    
    const rect = sliderEl.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let percent;
    
    if (x > rect.width) {
        const extra = x - rect.width;
        percent = 1.0 + (extra / rect.width) * 0.5;
    } else {
        percent = x / rect.width;
    }
    percent = Math.max(0, Math.min(1, percent));
    
    audio.volume = percent;
    audio.dataset.volume = percent;
    
    const fill = sliderEl.querySelector('.audio-volume-fill');
    if (fill) {
        fill.style.width = (percent * 100) + '%';
    }
    
    const volBtn = sliderEl.parentElement.querySelector('.audio-volume-btn');
    if (volBtn) volBtn.classList.toggle('muted', percent === 0);
}

function toggleMute(btn, nodeId) {
    const audio = document.getElementById('audio-' + nodeId);
    if (!audio) return;
    
    const currentVol = parseFloat(audio.dataset.volume) || 1;
    if (currentVol > 0) {
        audio.dataset.prevVolume = currentVol;
        audio.volume = 0;
    } else {
        audio.volume = audio.dataset.prevVolume || 1;
    }
    
    const player = btn.closest('.audio-player');
    const fill = player.querySelector('.audio-volume-fill');
    const vol = audio.volume;
    if (fill) {
        fill.style.width = (vol * 100) + '%';
    }
    btn.classList.toggle('muted', vol === 0);
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
}