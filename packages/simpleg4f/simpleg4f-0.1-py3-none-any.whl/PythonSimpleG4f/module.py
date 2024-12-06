from g4f.client import Client
import logging


class G4FClient:
    def __init__(self, model="gpt-4o-mini", image_model="flux"):
        """
        Инициализирует клиент для работы с G4F.
        :param model: Название модели для генерации текста (по умолчанию "gpt-4o-mini").
        :param image_model: Название модели для генерации изображений (по умолчанию "flux").
        """
        self.client = Client()
        self.model = model
        self.image_model = image_model
        self.logger = logging.getLogger(__name__)

    def send_message(self, message, additional_params=None):
        """
        Отправляет сообщение в G4F и получает ответ.
        :param message: Сообщение, которое будет отправлено модели.
        :param additional_params: Дополнительные параметры (опционально).
        :return: Ответ от модели.
        """
        try:
            # Подготовка запроса
            prompt = {"role": "user", "content": message}
            if additional_params:
                # Если есть дополнительные параметры, добавляем их в запрос
                prompt.update(additional_params)

            # Отправка запроса
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[prompt]
            )

            # Возвращаем сгенерированный ответ
            return response.choices[0].message.content.strip()

        except Exception as e:
            self.logger.error(f"Ошибка при отправке запроса: {e}")
            return f"Ошибка: {e}"

    def set_model(self, model_name):
        """
        Устанавливает новую модель для генерации текста.
        :param model_name: Название модели.
        """
        self.model = model_name
        self.logger.info(f"Модель изменена на: {model_name}")

    def generate_image(self, prompt):
        """
        Генерирует изображение на основе текстового запроса.
        :param prompt: Описание изображения, которое будет сгенерировано.
        :return: URL сгенерированного изображения.
        """
        try:
            # Отправка запроса на генерацию изображения
            response = self.client.images.generate(
                model=self.image_model,
                prompt=prompt
            )

            # Возвращаем URL сгенерированного изображения
            return response.data[0].url

        except Exception as e:
            self.logger.error(f"Ошибка при генерации изображения: {e}")
            return f"Ошибка: {e}"