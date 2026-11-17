// Hero background: domain-warped noise shader reacting to the cursor.
// Exposes window.heroGL = { setScroll(0..1) }. Falls back to the CSS gradient on #gl if WebGL is unavailable.
(function () {
  const canvas = document.getElementById('gl');
  const gl = canvas.getContext('webgl', { antialias: false, alpha: false });
  window.heroGL = { setScroll() {} };
  if (!gl) return;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const vert = `attribute vec2 p; void main(){ gl_Position = vec4(p, 0.0, 1.0); }`;
  const frag = `
    precision highp float;
    uniform vec2 uRes; uniform float uTime; uniform vec2 uMouse; uniform float uScroll;
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float noise(vec2 p){
      vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash(i), hash(i + vec2(1,0)), u.x), mix(hash(i + vec2(0,1)), hash(i + vec2(1,1)), u.x), u.y);
    }
    float fbm(vec2 p){ float v = 0.0, a = 0.5; for (int i = 0; i < 5; i++){ v += a * noise(p); p *= 2.02; a *= 0.5; } return v; }
    void main(){
      vec2 uv = gl_FragCoord.xy / uRes;
      vec2 p = (gl_FragCoord.xy - 0.5 * uRes) / uRes.y;
      vec2 m = (uMouse - 0.5) * vec2(uRes.x / uRes.y, 1.0);
      float d = length(p - m);
      float t = uTime * 0.05;
      vec2 q = vec2(fbm(p * 1.6 + t), fbm(p * 1.6 - t + 3.1));
      vec2 r = vec2(fbm(p * 1.4 + q * 2.0 + vec2(1.7, 9.2) + t * 1.3), fbm(p * 1.4 + q * 2.0 + vec2(8.3, 2.8) - t));
      float f = fbm(p * 1.2 + r * 1.8 + 0.5 * exp(-d * 3.0));
      vec3 bg = vec3(0.035, 0.035, 0.043);
      vec3 lime = vec3(0.78, 1.0, 0.24);
      vec3 violet = vec3(0.42, 0.27, 1.0);
      vec3 col = mix(bg, violet * 0.75, smoothstep(0.3, 0.85, f));
      col = mix(col, lime * 0.9, smoothstep(0.45, 0.9, f * r.x * 1.6));
      col += lime * 0.18 * exp(-d * 4.0);
      col += (hash(gl_FragCoord.xy + fract(uTime)) - 0.5) * 0.05;
      col *= 1.0 - 0.6 * length(uv - 0.5);
      col *= 1.0 - uScroll * 0.85;
      gl_FragColor = vec4(col, 1.0);
    }`;

  function shader(type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  let prog;
  try {
    prog = gl.createProgram();
    gl.attachShader(prog, shader(gl.VERTEX_SHADER, vert));
    gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, frag));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  } catch (e) { console.warn('WebGL shader failed, using CSS fallback', e); return; }
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'p');
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

  const u = name => gl.getUniformLocation(prog, name);
  const uRes = u('uRes'), uTime = u('uTime'), uMouse = u('uMouse'), uScroll = u('uScroll');

  // Render at reduced resolution: the shader is soft, so this is visually identical and much cheaper.
  // Cap the buffer at ~900px wide: on large screens a fixed 0.5 scale still means millions of shader runs per frame.
  let SCALE = 0.5;
  function resize() {
    SCALE = Math.min(0.5, 720 / innerWidth);
    canvas.width = Math.max(1, Math.round(innerWidth * SCALE));
    canvas.height = Math.max(1, Math.round(innerHeight * SCALE));
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uRes, canvas.width, canvas.height);
  }
  resize();
  addEventListener('resize', resize);

  const mouse = { x: 0.65, y: 0.6 }, target = { x: 0.65, y: 0.6 };
  addEventListener('pointermove', e => { target.x = e.clientX / innerWidth; target.y = 1 - e.clientY / innerHeight; });

  let scroll = 0, running = true;
  window.heroGL.setScroll = v => {
    scroll = Math.min(1, Math.max(0, v));
    const shouldRun = scroll < 1;
    if (shouldRun && !running) { running = true; requestAnimationFrame(frame); }
    running = shouldRun;
    if (!running) draw(performance.now());
  };

  function draw(now) {
    mouse.x += (target.x - mouse.x) * 0.05;
    mouse.y += (target.y - mouse.y) * 0.05;
    gl.uniform1f(uTime, reduce ? 20 : now / 1000);
    gl.uniform2f(uMouse, mouse.x, mouse.y);
    gl.uniform1f(uScroll, scroll);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  // The shader moves slowly, so 30fps looks the same and halves GPU work.
  let lastDraw = 0;
  function frame(now) {
    if (!running) return;
    if (now - lastDraw >= 32) { draw(now); lastDraw = now; }
    if (!reduce) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
