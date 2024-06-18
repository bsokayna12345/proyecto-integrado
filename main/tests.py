from django.test import TestCase
from django.urls import reverse
from .models import Pedido_cabecera, Pedido_detalle, Direccion
from django.contrib.auth.models import User


class ModeloTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.direccion = Direccion.objects.create(
            user_id=self.user,
            pais="Test Country",
            direccion="Test Address",
            provincia="Test Province",
            codigo_postal="12345"
        )
        self.pedido_cabecera = Pedido_cabecera.objects.create(
            usuario_id=self.user,
            direccion_entrega_id=self.direccion,
            order_id="ORDER123"
        )

    def test_crear_pedido_cabecera(self):
        self.assertEqual(self.pedido_cabecera.usuario_id.username, 'testuser')
        self.assertEqual(self.pedido_cabecera.direccion_entrega_id.pais, "Test Country")

    def test_str_pedido_cabecera(self):
        self.assertEqual(str(self.pedido_cabecera), f"{self.user}_1")
