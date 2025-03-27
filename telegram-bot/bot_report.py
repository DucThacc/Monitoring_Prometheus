#!/usr/bin/env python3
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Cấu hình Prometheus và bot
PROMETHEUS_URL = "http://192.168.253.128:9090"  # Địa chỉ Prometheus trên máy ảo
BOT_TOKEN = "7920437249:AAFHucmnlKgeqkd-n19xFoM8aiBP-oR-NYg"  # Thay bằng token bot của bạn
CHAT_ID = 6793955595  # Chat ID (đã lấy từ getUpdates)

def get_metric(query: str):
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {"query": query}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data["status"] == "success" and data["data"]["result"]:
            return data["data"]["result"][0]["value"][1]
        else:
            return "N/A"
    except Exception as e:
        return f"Error: {e}"

def check(update: Update, context: CallbackContext):
    # Lấy số liệu từ Prometheus
    cpu_busy = get_metric("100 - (avg by(instance) (rate(node_cpu_seconds_total{mode='idle'}[1m])) * 100)")
    sys_load = get_metric("node_load1")
    ram_used = get_metric("(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100")
    disk_used = get_metric("100 - (node_filesystem_free_bytes{mountpoint='/'} / node_filesystem_size_bytes{mountpoint='/'}) * 100")
    net_in = get_metric("rate(node_network_receive_bytes_total[1m])")
    net_out = get_metric("rate(node_network_transmit_bytes_total[1m])")
    
    report = (
        f"📊 *System Report*\n"
        f"CPU Busy: {cpu_busy}%\n"
        f"Load (1m): {sys_load}\n"
        f"RAM Used: {ram_used}%\n"
        f"Disk Used (/): {disk_used}%\n"
        f"Network In: {net_in} B/s\n"
        f"Network Out: {net_out} B/s\n"
    )
    update.message.reply_text(report, parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("check", check))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
