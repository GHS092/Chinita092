import sys

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_tag = '<!-- Evaluator Tab -->'
end_tag = '<!-- Chat Tab (Fixed to bottom) -->'

start_idx = content.find(start_tag)
end_idx = content.find(end_tag)

if start_idx != -1 and end_idx != -1:
    new_html = """<!-- Evaluator Tab -->
        <div class="hermes-eval-container" x-show="hermesState.activeTab === 'evaluator'">
          
          <h3 style="margin-bottom: 12px; font-size: 16px; color: #f8fafc; display: flex; justify-content: space-between; align-items: center;">
              <span style="display:flex; align-items:center; gap:8px;">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                  Custom Rubric (Text Input)
              </span>
              <span style="font-size: 12px; color: #64748b; background: rgba(0,0,0,0.3); padding: 4px 10px; border-radius: 20px;">Autosaving</span>
          </h3>
          <textarea 
            x-model="hermesState.rubricText" 
            @input="saveRubricText()" 
            style="width: 100%; height: 180px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; color: white; padding: 16px; font-family: var(--font-sans); font-size: 14px; resize: vertical; margin-bottom: 32px;"
            placeholder="Pega aquí el texto de la rúbrica...">
          </textarea>

          <h2 style="margin-bottom: 8px;">Analysis Engine</h2>
          <p style="color: #64748b; margin-bottom: 24px; font-size: 14px;">Hermes evaluará el video y la rúbrica usando IA.</p>
          
          <div class="yt-input-container">
            <input type="text" class="yt-input" x-model="hermesState.url" placeholder="https://youtube.com/watch?v=...">
            <button class="yt-btn" @click="evaluateVideo()" :disabled="hermesState.loading">
              <span x-show="!hermesState.loading">Initialize Run 🚀</span>
              <span x-show="hermesState.loading" style="display: flex; align-items: center; gap: 8px;">
                  <svg class="animate-spin" style="width: 18px; height: 18px; animation: spin 1s linear infinite;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  Processing...
              </span>
            </button>
          </div>
          
          <div x-show="hermesState.error" style="color: #fca5a5; margin-bottom: 24px; padding: 16px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 12px; font-family: monospace;" x-text="hermesState.error"></div>
          
          <!-- Loading Skeleton (Side-by-side) -->
          <div class="eval-layout" x-show="hermesState.loading && !hermesState.result">
            <div class="eval-left">
               <div class="eval-video-box skeleton"></div>
               <div class="eval-transcript-box skeleton" style="height: 150px"></div>
            </div>
            <div class="eval-right">
               <div class="eval-global-score skeleton" style="height: 100px"></div>
               <div class="eval-criteria-list">
                 <div class="skeleton" style="height: 120px; border-radius: 12px; width: 100%"></div>
                 <div class="skeleton" style="height: 120px; border-radius: 12px; width: 100%"></div>
               </div>
            </div>
          </div>

          <!-- Results Side-by-Side Layout -->
          <div class="eval-layout" x-show="hermesState.result && !hermesState.loading">
            <!-- Left Column -->
            <div class="eval-left">
               <!-- Video Player -->
               <div class="eval-video-box">
                  <template x-if="getYoutubeId(hermesState.url)">
                     <iframe :src="'https://www.youtube.com/embed/' + getYoutubeId(hermesState.url)" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                  </template>
                  <template x-if="!getYoutubeId(hermesState.url)">
                     <div>No valid YouTube URL detected</div>
                  </template>
               </div>
               
               <!-- Transcript -->
               <div class="eval-transcript-box" x-show="hermesState.result.transcript">
                  <h4>
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                    Transcripción de Voz / Discurso
                  </h4>
                  <div class="eval-transcript-text" x-text="hermesState.result.transcript"></div>
               </div>

               <!-- Vocabulary -->
               <div class="eval-vocabulary-box" x-show="hermesState.result.vocabulary_detected">
                  <h4>Vocabulario Integrado</h4>
                  
                  <div class="vocab-detected">
                     <h5>✓ VOCABULARIO UTILIZADO</h5>
                     <div class="vocab-badges">
                        <template x-for="word in hermesState.result.vocabulary_detected">
                           <span class="vocab-badge-green" x-text="word"></span>
                        </template>
                        <template x-if="!hermesState.result.vocabulary_detected || hermesState.result.vocabulary_detected.length === 0">
                           <span style="color:#64748b; font-size:12px;">Ninguno detectado</span>
                        </template>
                     </div>
                  </div>

                  <div class="vocab-missing" x-show="hermesState.result.vocabulary_missing && hermesState.result.vocabulary_missing.length > 0">
                     <h5>✗ VOCABULARIO NO DETECTADO / OMITIDO</h5>
                     <div class="vocab-badges">
                        <template x-for="word in hermesState.result.vocabulary_missing">
                           <span class="vocab-badge-red" x-text="word"></span>
                        </template>
                     </div>
                  </div>
               </div>
            </div>

            <!-- Right Column -->
            <div class="eval-right">
               <!-- Global Score -->
               <div class="eval-global-score">
                  <div class="global-score-left">
                     <div class="global-score-header">EVALUACIÓN GLOBAL CALCULADA</div>
                     <div class="global-score-name">Reporte Activo</div>
                     <div class="global-score-sub" x-text="'Generado automáticamente por IA • ' + new Date().toLocaleDateString()"></div>
                  </div>
                  <div class="global-score-right">
                     <div style="font-size: 11px; color: #94a3b8; font-weight: 700; letter-spacing: 1px; margin-bottom: 4px;">PUNTAJE TOTAL</div>
                     <div class="global-score-value">
                        <span style="font-size: 28px;">🏅</span>
                        <span x-text="calculateTotalScore(hermesState.result)"></span>
                        <span class="max-pts" x-text="'/ ' + calculateMaxScore(hermesState.result)"></span>
                     </div>
                  </div>
               </div>

               <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:12px; margin-top: 8px;">
                  <div>
                     <h3 style="margin:0; font-size: 16px; color: white;">Calificación Detallada Rúbrica</h3>
                     <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Selecciona o acomoda puntajes. Los cambios se sumarán en tiempo real.</div>
                  </div>
                  <div style="color: #4ade80; font-size: 12px; font-weight: 600; display:flex; align-items:center; gap:4px;">
                     <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                     Suma Activa
                  </div>
               </div>

               <!-- Criteria List -->
               <div class="eval-criteria-list" x-show="hermesState.result.criteria">
                  <template x-for="(crit, i) in hermesState.result.criteria" :key="i">
                     <div class="criteria-row">
                        <div class="crit-header">
                           <div class="crit-number" x-text="i + 1"></div>
                           <div class="crit-name" x-text="crit.name"></div>
                           <div class="crit-pts" x-text="(crit.score || 0) + ' / ' + crit.max + ' pts'"></div>
                        </div>
                        <div class="crit-score-buttons">
                           <template x-for="pts in getScoreOptions(parseFloat(crit.max))">
                              <div class="score-btn-pill" :class="{active: parseFloat(crit.score) === parseFloat(pts)}" @click="crit.score = pts" x-text="pts + ' pts'"></div>
                           </template>
                        </div>
                        <div class="crit-feedback">
                           <div class="crit-feedback-label">RETROALIMENTACIÓN IA:</div>
                           
                           <template x-if="typeof crit.feedback === 'object' && crit.feedback !== null">
                              <div>
                                 <div class="crit-feedback-text" x-text="crit.feedback.justification" style="margin-bottom: 12px;"></div>
                                 
                                 <template x-if="crit.feedback.errors && crit.feedback.errors.length > 0">
                                    <div style="margin-bottom: 12px; background: rgba(248, 113, 113, 0.05); padding: 12px; border-radius: 8px; border-left: 2px solid #f87171;">
                                       <div style="color: #fca5a5; font-size: 11px; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px;">❌ ERRORES / FALLAS IDENTIFICADAS:</div>
                                       <ul style="margin: 0; padding-left: 16px; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                                          <template x-for="err in crit.feedback.errors">
                                             <li x-text="err" style="margin-bottom: 4px;"></li>
                                          </template>
                                       </ul>
                                    </div>
                                 </template>

                                 <template x-if="crit.feedback.strengths && crit.feedback.strengths.length > 0">
                                    <div style="background: rgba(74, 222, 128, 0.05); padding: 12px; border-radius: 8px; border-left: 2px solid #4ade80;">
                                       <div style="color: #86efac; font-size: 11px; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px;">✅ FORTALEZAS DESTACADAS:</div>
                                       <ul style="margin: 0; padding-left: 16px; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                                          <template x-for="str in crit.feedback.strengths">
                                             <li x-text="str" style="margin-bottom: 4px;"></li>
                                          </template>
                                       </ul>
                                    </div>
                                 </template>
                              </div>
                           </template>

                           <template x-if="typeof crit.feedback === 'string'">
                              <div class="crit-feedback-text" x-text="crit.feedback"></div>
                           </template>

                        </div>
                     </div>
                  </template>
               </div>
            </div>
          </div>
        </div>
        
        """
    content = content[:start_idx] + new_html + content[end_idx:]
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: HTML Replaced.")
else:
    print("ERROR: Could not find tags.")
    print("Start:", start_idx)
    print("End:", end_idx)
