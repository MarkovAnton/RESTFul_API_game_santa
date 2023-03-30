from flask import Flask, json
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api()

groups = []


class Group(Resource):
    def post(self):
        group_id = len(groups) + 1
        participants = []
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        params = parser.parse_args()
        for group in groups:
            if group["name"] == params["name"]:
                return f'Group with name {params["name"]} already exists', 400
        group = {
            "id": group_id,
            "name": params["name"],
            "description": params["description"],
            "participants": participants
        }
        groups.append(group)
        return group_id, 201


class Groups(Resource):
    def get(self):
        groups_no_part = []
        for group in groups:
            group = {
                "id": group["id"],
                "name": group["name"],
                "description": group["description"]
            }
            groups_no_part.append(group)
        return groups_no_part, 200


class Group_id(Resource):
    def get(self, group_id):
        for group in groups:
            if group["id"] == group_id:
                return group, 200
        return "Group not found", 404

    def put(self, group_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        params = parser.parse_args()
        for group in groups:
            if group["id"] == group_id:
                group["name"] = params["name"]
                group["description"] = params["description"]
                return group, 200

        group = {
            "id": group_id,
            "name": params["name"],
            "description": params["description"]
        }
        groups.append(group)
        return group, 201

    def delete(self, group_id):
        global groups
        groups = [group for group in groups if group["id"] != group_id]
        return f'Group with id {group_id} is deleted.', 200


class Group_id_participant(Resource):
    def post(self, group_id):
        recipient = []
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("wish", type=str)
        params = parser.parse_args()
        for group in groups:
            if group["id"] == group_id:
                part_id = len(group["participants"]) + 1
                for participant in group["participants"]:
                    if participant["name"] == params["name"]:
                        return f'Participant with name {params["name"]} already exists', 400
                participant = {
                    "id": part_id,
                    "name": params["name"],
                    "wish": params["wish"],
                    "recipient": recipient
                }
                group["participants"].append(participant)
                return part_id, 201


class Group_id_participant_id(Resource):
    def delete(self, group_id, participant_id):
        for group in groups:
            if group["id"] == group_id:
                group["participants"] = [participant for participant in group["participants"]
                                         if participant["id"] != participant_id]
                return f'Participant with id {participant_id} is deleted.', 200


class Group_id_toss(Resource):
    def post(self, group_id):
        for group in groups:
            if group["id"] == group_id:
                if len(group["participants"]) >= 3:
                    participants_and_recipients = group["participants"]
                    for participant in group["participants"]:
                        participants_and_recipients = [part for part in participants_and_recipients
                                                       if part != participant]
                        if len(participants_and_recipients) <= 1:
                            return group["participants"]
                        recipient_rand = random.choice(participants_and_recipients)
                        if recipient_rand in participants_and_recipients:
                            participant["recipient"] = recipient_rand
                            participants_and_recipients = [part for part in participants_and_recipients
                                                           if part != recipient_rand]
                else:
                    return f'Drawing lots for a group with an id {group_id} is not possible.', 409


class Group_id_participant_id_recipient(Resource):
    def get(self, group_id, participant_id):
        for group in groups:
            if group["id"] == group_id:
                for participant in group["participants"]:
                    if participant["id"] == participant_id:
                        recipient = participant["recipient"]
                        recipient = {
                            "id": recipient["id"],
                            "name": recipient["name"],
                            "wish": recipient["wish"]
                        }
                        return recipient


api.add_resource(Group, "/group")
api.add_resource(Groups, "/groups")
api.add_resource(Group_id, "/group/<int:group_id>")
api.add_resource(Group_id_participant, "/group/<int:group_id>/participant")
api.add_resource(Group_id_participant_id, "/group/<int:group_id>/participant/<int:participant_id>")
api.add_resource(Group_id_toss, "/group/<int:group_id>/toss")
api.add_resource(Group_id_participant_id_recipient, "/group/<int:group_id>/participant/<int:participant_id>/recipient")
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="127.0.0.1")

