---
title: Pi Monte Carlo
---

.. raw:: html
    
    <script src="/static/gen/pimontecarlo.js" type="module"></script>
    <div id="app">
        <label for="samples_count">
            Samples count:

            <input type="number" name="samples_count" id="samples_count">
        </label>

        <label for="samples_in_circle">
            Samples in circle:

            <input type="number" name="samples_in_circle" id="samples_in_circle">
        </label>

        <label for="ratio">
            Ratio:

            <input type="number" name="ratio" id="ratio">
        </label>


        <canvas name="canvas" width="400" height=400></canvas>
    </div>


Code source disponible `ici <https://github.com/jtremesay/jtremesay.org/blob/main/front/main/pimontecarlo.ts>`_.