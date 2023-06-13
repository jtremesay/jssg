Chaînes Youtube
###############

:date: 2023-06-06 20:00

Une sélection de chaînes Youtube dumpées de mon agrégateur de flux. Généré automatiquement depuis `youtube_channels.csv <{static}static/files/youtube_channels.csv>`_:


.. raw:: html

    <table>
        <thead>
            <tr>
                <th>Nom</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
{% for chaine in "content/static/files/youtube_channels.csv"|read_csv  %}
                <td><a href="{{ chaine.url }}">{{ chaine.title }}</a></td>
                <td>{{ chaine.description }}</td>
            </tr>
{% endfor %}
        </tbody>
    </table>