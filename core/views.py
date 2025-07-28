from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from .models import Conversation
from .serializers import ConversationSerializer
from django.shortcuts import render
import json
from collections import Counter

class VegetarianConversationsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        veg_conversations = Conversation.objects.filter(is_vegetarian=True)
        serializer = ConversationSerializer(veg_conversations, many=True)
        return Response(serializer.data)


class AllConversationsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


class APIRootView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "stats": "/stats/",
            "all_conversations": "/api/conversations/",
            "vegetarian_conversations": "/api/vegetarian_conversations/",
            "admin": "/admin/",
        })


class StatsView(View):
    def get(self, request):
        responses = Conversation.objects.all()
        total_responses = responses.count()

        if total_responses == 0:
            context = {
                "total": 0,
                "vegetarian": 0,
                "non_vegetarian": 0,
                "veg_percentage": 0,
                "non_veg_percentage": 0,
                "food_labels": json.dumps([]),
                "food_values": json.dumps([]),
                "insights": ["No data available yet."]
            }
            return render(request, "stats/stats.html", context)

        vegetarian_count = responses.filter(is_vegetarian=True).count()
        non_vegetarian_count = total_responses - vegetarian_count

        veg_percentage = round((vegetarian_count / total_responses) * 100, 1)
        non_veg_percentage = round((non_vegetarian_count / total_responses) * 100, 1)

        food_counter = Counter()
        for response in responses:
            if response.answer:
                try:
                    foods = [food.strip().lower() for food in response.answer.split(',') if food.strip()]
                    food_counter.update(foods)
                except (AttributeError, TypeError):
                    continue

        top_foods = food_counter.most_common(10)
        food_labels = [food.title() for food, count in top_foods]
        food_values = [count for food, count in top_foods]

        insights = []
        if veg_percentage > non_veg_percentage:
            insights.append(f"More people prefer vegetarian diet ({veg_percentage}%) than non-vegetarian.")
        elif veg_percentage < non_veg_percentage:
            insights.append(f"Non-vegetarian diet is more preferred ({non_veg_percentage}%).")
        else:
            insights.append("Equal preference for vegetarian and non-vegetarian diets.")

        if food_labels:
            insights.append(f"Top mentioned food: {food_labels[0]} with {food_values[0]} mentions.")

        context = {
            "total": total_responses,
            "vegetarian": vegetarian_count,
            "non_vegetarian": non_vegetarian_count,
            "veg_percentage": veg_percentage,
            "non_veg_percentage": non_veg_percentage,
            "food_labels": json.dumps(food_labels),
            "food_values": json.dumps(food_values),
            "insights": insights,
        }

        return render(request, "stats/stats.html", context)
