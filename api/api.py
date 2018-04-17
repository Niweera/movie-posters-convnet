from src.db_manager import (get_db, Poster)
from src.utils import read_config
from flask_restful import Resource


class ApiPosters(Resource):
    def __init__(self, path_config='./config/development.conf'):
        self.config = read_config(path_config)
        self.db = get_db(self.config['general']['db_uri'])

    def get_movie_by_id(self, id, fields):
        print('entering get_movie_by_id')
        result = self.db.query(fields).filter_by(id=id).first()._asdict()
        print('result: {}'.format(result))
        return result

    def get(self, id):
        """ Retrieve the movie poster with specific id along with
        its closest movie posters
        """
        id = int(id)
        print('movie id: {}'.format(id))
        fields = (Poster.closest_posters)
        ids_closest = self.get_movie_by_id(id, fields)

        ids = [id]
        ids += [int(x) for x in ids_closest['closest_posters'].split(',')]
        fields = (Poster.title_display,
                  Poster.url_img,
                  Poster.closest_posters)

        data = [self.get_movie_by_id(x, *fields) for x in ids]
        return data
