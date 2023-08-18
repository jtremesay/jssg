---
title: Tris animés
---

Un truc much en vanilla TS pour visualiser les algos de tris.

.. raw:: html
    
    <script src="/static/gen/sorts.js" type="module"></script>
    <div id="app">
        <div>

        <label for="sort">
            Sort:
            <select name="sort" id="sort">
            </select>
        </label>

        <label for="samples_count">
            <code>log2(</code>Samples count <code>)</code>:

            <input type="number" name="samples_count" id="samples_count" min="1" max="10" value="6">
        </label>

        <label for="reset">
            <input type="button" name="reset" id="reset" value="Reset">
        </label>

        <label for="playback">
            Playback:
            <input type="checkbox" name="playback" id="playback" checked>
        </label>

        </div>
        <canvas name="canvas" width="640" height="480"></canvas>
    </div>


Code source disponible `ici <https://github.com/jtremesay/jtremesay.org/blob/main/front/main/sorts.ts>`_.